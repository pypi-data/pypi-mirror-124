from typing import Any, Dict, List

from pandas import DataFrame

from cognite.well_model.client.models.depth_measurement_rows import DepthMeasurementRows
from cognite.well_model.client.models.trajectory_rows import TrajectoryRows
from cognite.well_model.models import (
    CasingSchematic,
    DepthMeasurement,
    MnemonicMatchGroup,
    Nds,
    Npt,
    SummaryCount,
    TimeMeasurement,
    Trajectory,
    Well,
    Wellbore,
    WellTops,
)


class WDLResourceList:
    _RESOURCE = None

    def __init__(self, resources: List[Any]):
        self.data = resources
        for resource in resources:
            if resource is None or not isinstance(resource, self._RESOURCE):  # type: ignore
                raise TypeError(
                    f"All resources for class '{self.__class__.__name__}' must be of type"  # type: ignore
                    f" '{self._RESOURCE.__name__}', "
                    f"not '{type(resource)}'. "
                )

    def dump(self, camel_case: bool = False) -> List[Dict[str, Any]]:
        """Dump the instance into a json serializable Python data type.

        Args:
            camel_case (bool): Use camelCase for attribute names. Defaults to False.

        Returns:
            List[Dict[str, Any]]: A list of dicts representing the instance.
        """
        return [resource.dump(camel_case=camel_case) for resource in self.data]

    def to_pandas(self, camel_case=True) -> DataFrame:
        return DataFrame(self.dump(camel_case=camel_case))

    def _repr_html_(self):
        return self.to_pandas(camel_case=True)._repr_html_()

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self):
        return self.data.__iter__()

    def __repr__(self):
        return_string = [object.__repr__(d) for d in self.data]
        return f"[{', '.join(r for r in return_string)}]"

    def __len__(self):
        return self.data.__len__()


class WellList(WDLResourceList):
    _RESOURCE = Well


class WellboreList(WDLResourceList):
    _RESOURCE = Wellbore


class NptList(WDLResourceList):
    _RESOURCE = Npt


class TrajectoryList(WDLResourceList):
    _RESOURCE = Trajectory


class TrajectoryDataList(WDLResourceList):
    _RESOURCE = TrajectoryRows


class NdsList(WDLResourceList):
    _RESOURCE = Nds


class DepthMeasurementList(WDLResourceList):
    _RESOURCE = DepthMeasurement


class DepthMeasurementDataList(WDLResourceList):
    _RESOURCE = DepthMeasurementRows


class TimeMeasurementList(WDLResourceList):
    _RESOURCE = TimeMeasurement


class CasingsList(WDLResourceList):
    _RESOURCE = CasingSchematic


class WellTopsList(WDLResourceList):
    _RESOURCE = WellTops

    def to_pandas(self, camel_case=True):
        rows = [
            {
                "wellboreMatchingId": welltop.wellbore_matching_id,
                "wellboreName": welltop.wellbore_name,
                "sequenceExternalId": welltop.source.sequence_external_id,
                "sourceName": welltop.source.source_name,
                "tops_count": len(welltop.tops),
            }
            for welltop in self.data
        ]
        return DataFrame(rows)


class MnemonicMatchList(WDLResourceList):
    _RESOURCE = MnemonicMatchGroup

    def to_pandas(self, camel_case=True):
        matches = []
        for group in self.data:
            for match in group.matches:
                tools = [x.code for x in match.tools]
                matches.append(
                    {
                        "mnemonic": group.mnemonic,
                        "companyName": match.company_name,
                        "measurementType": match.measurement_type,
                        "primaryQuantityClass": match.primary_quantity_class,
                        "tools": tools,
                    }
                )
        if len(matches) > 0:
            return DataFrame(matches)

        return DataFrame(
            {
                "mnemonic": [],
                "companyName": [],
                "measurementType": [],
                "primaryQuantityClass": [],
                "tools": [],
            }
        )


class SummaryList(WDLResourceList):
    _RESOURCE = SummaryCount
