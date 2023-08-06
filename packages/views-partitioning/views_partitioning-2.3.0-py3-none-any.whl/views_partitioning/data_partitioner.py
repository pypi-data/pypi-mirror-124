from typing import Callable, List, Dict, Tuple, TypeVar, Union
import views_schema
import pandas as pd
from . import legacy

T = TypeVar("T")
NestedDicts = Dict[str,Dict[str,T]]
TimePeriodGetter = NestedDicts[Callable[[pd.DataFrame], pd.DataFrame]]
PartitionsDicts = NestedDicts[Tuple[int,int]]

gtzero = lambda x: x if x > 0 else 0

class DataPartitioner():

    def __init__(self, partitions: Union[PartitionsDicts, views_schema.Partitions]):
        if isinstance(partitions, dict):
            partitions = views_schema.Partitions.from_dict(partitions)

        self.partitions = partitions

    def _map(self, fn):
        return DataPartitioner(self.partitions.map(fn))

    def _pmap(self, fn):
        return DataPartitioner(self.partitions.pmap(fn))

    def _pad(self, size: int):
        sub_from_start = abs(size) if size < 0 else 0
        add_to_end = size if size > 0 else 0
        return self._map(lambda s,e: (s - sub_from_start, e + add_to_end))

    def _trim(self, size: int):
        add_to_start = size if size > 0 else 0
        sub_from_end = abs(size) if size < 0 else 0
        return self._map(lambda s,e: (s + add_to_start, e - sub_from_end))

    def trim(self, size):
        return self._trim(-gtzero(size))

    def ltrim(self, size):
        return self._trim(gtzero(size))

    def pad(self, size: int):
        size = size if size > 0 else 0
        return self._pad(size)

    def lpad(self, size: int):
        size = size if size > 0 else 0
        return self._pad(-size)

    def no_overlap(self, rev:bool = False):
        return self._pmap(lambda p: p.no_overlap(rev = rev))

    def in_extent(self, start, end):
        return self._map(lambda s,e: (s if s > start else start, e if e < end else end))

    def extent(self):
        return self.partitions.extent()

    def shift_left(self, size: int) -> 'DataPartitioner':
        start,end = self.extent()
        return (self
                .lpad(size)
                .no_overlap(rev = True)
                .in_extent(start, end))

    def shift_right(self, size: int)-> 'DataPartitioner':
        start,end = self.extent()
        return (self
                .pad(size)
                .no_overlap()
                .in_extent(start, end))

    def __call__(self,
            partition_name: str,
            time_period_name: str,
            data: pd.DataFrame)-> pd.DataFrame:
        timespan = self.partitions.partitions[partition_name].timespans[time_period_name]
        return data.loc[timespan.start : timespan.end, :]

    @classmethod
    def from_legacy_periods(cls, periods: List[legacy.Period]):
        for p in periods:
            try:
                legacy.period_object_is_valid(p)
            except AssertionError:
                raise ValueError(f"Period {p} is not a valid time period object")

        partitions = {}
        for period in periods:
            partitions[period.name] = {
                    "train": (period.train_start, period.train_end),
                    "predict": (period.predict_start, period.predict_end),
                    }

        return cls(partitions)
