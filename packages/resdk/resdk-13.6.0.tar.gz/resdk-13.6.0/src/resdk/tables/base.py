""".. Ignore pydocstyle D400.

===========
Base Tables
===========

.. autoclass:: BaseTables
    :members:

    .. automethod:: __init__

"""
import abc
import asyncio
import json
import os
from functools import lru_cache
from io import BytesIO
from typing import Callable, List, Optional
from urllib.parse import urljoin

import aiohttp
import pandas as pd
import pytz
from tqdm import tqdm

from resdk.resolwe import Resolwe
from resdk.resources import Collection, Data, Sample
from resdk.resources.utils import iterate_schema
from resdk.utils.table_cache import (
    cache_dir_resdk,
    clear_cache_dir_resdk,
    load_pickle,
    save_pickle,
)

SAMPLE_FIELDS = [
    "id",
    "slug",
    "name",
    "descriptor",
    "descriptor_schema",
]
DATA_FIELDS = [
    "id",
    "slug",
    "modified",
    "entity__name",
    "entity__id",
    "output",
    "process__output_schema",
    "process__slug",
]

# See _download_data function for in-depth explanation of this.
EXP_ASYNC_CHUNK_SIZE = 50


class TqdmWithCallable(tqdm):
    """Tqdm class that also calls a given callable."""

    def __init__(self, *args, **kwargs):
        """Initialize class."""
        self.callable = kwargs.pop("callable", None)
        super().__init__(*args, **kwargs)

    def update(self, n=1):
        """Update."""
        super().update(n=n)
        if self.callable:
            self.callable(self.n / self.total)


class BaseTables(abc.ABC):
    """A base class for *Tables."""

    process_type = None
    META = "meta"

    def __init__(
        self,
        collection: Collection,
        cache_dir: Optional[str] = None,
        progress_callable: Optional[Callable] = None,
    ):
        """Initialize class.

        :param collection: collection to use
        :param cache_dir: cache directory location, if not specified system specific
                          cache directory is used
        :param progress_callable: custom callable that can be used to report
                                  progress. By default, progress is written to
                                  stderr with tqdm
        """
        self.resolwe = collection.resolwe  # type: Resolwe
        self.collection = collection

        self.tqdm = TqdmWithCallable
        self.progress_callable = progress_callable

        self.cache_dir = cache_dir
        if self.cache_dir is None:
            self.cache_dir = cache_dir_resdk()
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    @property
    @lru_cache()
    def meta(self) -> pd.DataFrame:
        """Return samples metadata table as a pandas DataFrame object.

        :return: table of metadata
        """
        return self._load_fetch(self.META)

    @staticmethod
    def clear_cache() -> None:
        """Remove ReSDK cache files from the default cache directory."""
        clear_cache_dir_resdk()

    @property
    @lru_cache()
    def _samples(self) -> List[Sample]:
        """Fetch sample objects.

        Fetch all samples from given collection and cache the results in memory. Only
        the needed subset of fields is fetched.

        :return: list od Sample objects
        """
        sample_ids = [d.sample.id for d in self._data]
        return list(
            self.collection.samples.filter(id__in=sample_ids, fields=SAMPLE_FIELDS)
        )

    @property
    @lru_cache()
    def _data(self) -> List[Data]:
        """Fetch data objects.

        Fetch Data of type ``self.process_type`` from given collection
        and cache the results in memory. Only the needed subset of
        fields is fetched.

        :return: list of Data objects
        """
        kwargs = {
            "type": self.process_type,
            "fields": DATA_FIELDS,
        }
        return list(self.collection.data.filter(**kwargs))

    @property
    @lru_cache()
    def _metadata_version(self) -> str:
        """Return server metadata version.

        The versioning of metadata on the server is determined by the
        newest of these values:

            - newset modified sample
            - newset modified relation
            - newset modified orange Data

        :return: metadata version
        """
        timestamps = []
        kwargs = {
            "ordering": "-modified",
            "fields": ["id", "modified"],
            "limit": 1,
        }

        try:
            newest_sample = self.collection.samples.get(**kwargs)
            timestamps.append(newest_sample.modified)
        except LookupError:
            raise ValueError(
                f"Collection {self.collection.name} has no samples!"
            ) from None

        try:
            newest_relation = self.collection.relations.get(**kwargs)
            timestamps.append(newest_relation.modified)
        except LookupError:
            pass

        try:
            orange = self._get_orange_object()
            timestamps.append(orange.modified)
        except LookupError:
            pass

        newest_modified = sorted(timestamps)[-1]
        # transform into UTC so changing timezones won't effect cache
        version = (
            newest_modified.astimezone(pytz.utc).isoformat().replace("+00:00", "Z")
        )
        return version

    @property
    @lru_cache()
    def _data_version(self) -> str:
        """Return server data version.

        The versioning of Data on the server is determined by the hash of
        the tuple of sorted data objects ids.

        :return: data version
        """
        if len(self._data) == 0:
            raise ValueError(
                f"Collection {self.collection.name} has no {self.process_type} data!"
            )
        data_ids = tuple(sorted(d.id for d in self._data))
        version = str(hash(data_ids))
        return version

    def _load_fetch(self, data_type: str) -> pd.DataFrame:
        """Load data from disc or fetch it from server and cache it on disc."""
        data = load_pickle(self._cache_file(data_type))
        if data is None:
            if data_type == self.META:
                data = self._download_metadata()
            else:
                # XXX: When dropping support for Python 3.6 the below
                # statement can be replaced with:
                # data = asyncio.run(self._download_data(data_type))
                loop = asyncio.get_event_loop()
                data = loop.run_until_complete(self._download_data(data_type))

            save_pickle(data, self._cache_file(data_type))
        return data

    @abc.abstractmethod
    def _cache_file(self, data_type: str) -> str:
        """Return full cache file path."""
        pass

    def _get_descriptors(self) -> pd.DataFrame:
        descriptors = []
        for sample in self._samples:
            sample.descriptor["sample_name"] = sample.name
            descriptors.append(sample.descriptor)

        df = pd.json_normalize(descriptors).set_index("sample_name")

        # Keep only numeric / string types:
        column_types = {}
        prefix = "XXX"
        for (schema, _, path) in iterate_schema(
            sample.descriptor, sample.descriptor_schema.schema, path=prefix
        ):
            field_type = schema["type"]
            field_name = path[len(prefix) + 1 :]

            # This can happen if this filed has None value in all descriptors
            if field_name not in df:
                continue

            if field_type == "basic:string:":
                column_types[field_name] = str
            elif field_type == "basic:integer:":
                # Pandas cannot cast NaN's to int, but it can cast them
                # to pd.Int64Dtype
                column_types[field_name] = pd.Int64Dtype()
            elif field_type == "basic:decimal:":
                column_types[field_name] = float

        df = df[column_types.keys()].astype(column_types)

        return df

    def _get_relations(self) -> pd.DataFrame:
        relations = pd.DataFrame(index=[s.name for s in self._samples])
        relations.index.name = "sample_name"

        id_to_name = {s.id: s.name for s in self._samples}

        for relation in self.collection.relations.filter():
            # Only consider relations that include only samples in self.samples
            relation_entities_ids = set([p["entity"] for p in relation.partitions])
            if not relation_entities_ids.issubset({d.sample.id for d in self._data}):
                pass

            relations[relation.category] = pd.Series(
                index=relations.index, dtype="object"
            )

            for partition in relation.partitions:
                value = ""
                if partition["label"] and partition["position"]:
                    value = f'{partition["label"]} / {partition["position"]}'
                elif partition["label"]:
                    value = partition["label"]
                elif partition["position"]:
                    value = partition["position"]

                sample_name = id_to_name.get(partition["entity"], None)
                if sample_name:
                    relations[relation.category][sample_name] = value

        return relations

    @lru_cache()
    def _get_orange_object(self) -> Data:
        return self.collection.data.get(
            process__slug="upload-orange-metadata",
            ordering="-modified",
            fields=DATA_FIELDS,
            limit=1,
        )

    def _get_orange_data(self) -> pd.DataFrame:
        try:
            orange_meta = self._get_orange_object()
        except LookupError:
            return pd.DataFrame()

        file_name = orange_meta.files(field_name="table")[0]
        url = urljoin(self.resolwe.url, f"data/{orange_meta.id}/{file_name}")
        response = self.resolwe.session.get(url, auth=self.resolwe.auth)
        response.raise_for_status()

        with BytesIO() as f:
            f.write(response.content)
            f.seek(0)
            if file_name.endswith("xls"):
                df = pd.read_excel(f, engine="xlrd")
            elif file_name.endswith("xlsx"):
                df = pd.read_excel(f, engine="openpyxl")
            elif any(file_name.endswith(ext) for ext in ["tab", "tsv"]):
                df = pd.read_csv(f, sep="\t")
            elif file_name.endswith("csv"):
                df = pd.read_csv(f)
            else:
                # TODO: logging, warning?
                return pd.DataFrame()

        if "mS#Sample ID" in df.columns:
            mapping = {s.id: s.name for s in self._samples}
            df["sample_name"] = [mapping[value] for value in df["mS#Sample ID"]]
            df = df.drop(columns=["mS#Sample ID"])
        elif "mS#Sample slug" in df.columns:
            mapping = {s.slug: s.name for s in self._samples}
            df["sample_name"] = [mapping[value] for value in df["mS#Sample slug"]]
            df = df.drop(columns=["mS#Sample slug"])
        elif "mS#Sample name" in df.columns:
            df = df.rename(columns={"mS#Sample name": "sample_name"})

        return df.set_index("sample_name")

    def _download_metadata(self) -> pd.DataFrame:
        """Download samples metadata and transform into table."""
        meta = pd.DataFrame(None, index=[s.name for s in self._samples])

        # Add descriptors metadata
        descriptors = self._get_descriptors()
        meta = meta.merge(descriptors, how="right", left_index=True, right_index=True)

        # Add relations metadata
        relations = self._get_relations()
        how = "outer" if len(meta.columns) else "right"
        meta = meta.merge(relations, how=how, left_index=True, right_index=True)

        # Add Orange clinical metadata
        orange_data = self._get_orange_data()
        if not orange_data.empty:
            how = "right" if meta.columns.empty else "outer"
            meta = meta.merge(orange_data, how=how, left_index=True, right_index=True)

        meta = meta.sort_index()
        meta.index.name = "sample_name"

        return meta

    def _get_data_uri(self, data: Data, data_type: str) -> str:
        field_name = self.data_type_to_field_name[data_type]
        files = data.files(field_name=field_name)

        if not files:
            raise LookupError(f"Data {data.slug} has no files named {field_name}!")
        elif len(files) > 1:
            raise LookupError(
                f"Data {data.slug} has multiple files named {field_name}!"
            )

        return f"{data.id}/{files[0]}"

    def _get_data_urls(self, uris):
        response = self.resolwe.session.post(
            urljoin(self.resolwe.url, "resolve_uris/"),
            json={"uris": list(uris)},
            auth=self.resolwe.auth,
        )
        response.raise_for_status()
        return json.loads(response.content.decode("utf-8"))

    @abc.abstractmethod
    def _parse_file(self, file_obj, sample_name, data_type):
        """Parse file object and return a one DataFrame line."""
        pass

    async def _download_file(self, url, session, sample_name, data_type):
        async with session.get(url) as response:
            response.raise_for_status()
            with BytesIO() as f:
                f.write(await response.content.read())
                f.seek(0)
                sample_data = self._parse_file(f, sample_name, data_type)
        return sample_data

    async def _download_data(self, data_type: str) -> pd.DataFrame:
        """Download data files and marge them into a pandas DataFrame.

        During normal download of a single file a signed url is created on AWS
        and user is than redirected from Genialis server to the signed url.

        However, this process (signing urls and redirecting) takes time.
        To speedup things, we create a dedicated endpoint that accepts a bunch
        of file uris and return a bunch of signed url's. All in one request.

        However, these signed urls have expiration time of 60 s. In case of
        large number of uris requested (> 100 uris) it is likely that url is
        signed by Resolwe server and not downloaded for 60 seconds or more.
        Therefore we split the uris in smaller chunks, namely
        EXP_ASYNC_CHUNK_SIZE.

        :param data_type: data type
        :return: table with data, features in columns, samples in rows
        """
        samples_data = []
        for i in self.tqdm(
            range(0, len(self._data), EXP_ASYNC_CHUNK_SIZE),
            desc="Downloading data",
            ncols=100,
            file=open(os.devnull, "w") if self.progress_callable else None,
            callable=self.progress_callable,
        ):
            data_subset = self._data[i : i + EXP_ASYNC_CHUNK_SIZE]

            # Mapping from file uri to sample name
            uri_to_name = {
                self._get_data_uri(d, data_type): d._original_values["entity"]["name"]
                for d in data_subset
            }

            source_urls = self._get_data_urls(uri_to_name.keys())
            urls_names = [(url, uri_to_name[uri]) for uri, url in source_urls.items()]

            async with aiohttp.ClientSession() as session:
                futures = [
                    self._download_file(url, session, name, data_type)
                    for url, name in urls_names
                ]
                data = await asyncio.gather(*futures)
                samples_data.extend(data)

        df = pd.concat(samples_data, axis=1).T.sort_index().sort_index(axis=1)
        df.index.name = "sample_name"
        return df
