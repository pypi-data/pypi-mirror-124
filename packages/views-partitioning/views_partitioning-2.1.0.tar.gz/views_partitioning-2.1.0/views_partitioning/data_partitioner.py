from collections import defaultdict
from typing import Callable, List, Dict, Tuple, TypeVar, Union
import views_schema
import pandas as pd
from . import legacy

T = TypeVar("T")
NestedDicts = Dict[str,Dict[str,T]]
TimePeriodGetter = NestedDicts[Callable[[pd.DataFrame], pd.DataFrame]]
PartitionsDicts = NestedDicts[Tuple[int,int]]

class DataPartitioner():

    def __init__(self, partitions: Union[PartitionsDicts, views_schema.Partitions]):
        if isinstance(partitions, dict):
            partitions = views_schema.Partitions.from_dict(partitions)

        self.partitions = partitions

    def _pad(self, size: int):
        _old_partitions = self.partitions
        new_partitions = defaultdict(dict)
        sub_from_start = abs(size) if size < 0 else 0
        add_to_end = size if size > 0 else 0
        for partition_name, partition in self.partitions.partitions.items():
            for timespan_name, timespan in partition.timespans.items():
                new_partitions[partition_name][timespan_name] = (timespan.start - sub_from_start, timespan.end + add_to_end)
        return DataPartitioner(new_partitions)

    def pad(self, size: int):
        size = size if size > 0 else 0
        return self._pad(size)

    def lpad(self, size: int):
        size = size if size > 0 else 0
        return self._pad(-size)

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
