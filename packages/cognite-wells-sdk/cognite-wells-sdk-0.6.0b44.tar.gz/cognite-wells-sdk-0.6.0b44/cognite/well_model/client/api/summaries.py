import logging
from typing import List

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.models.resource_list import SummaryList
from cognite.well_model.models import Label, LabelItems

logger = logging.getLogger(__name__)


class SummariesAPI(BaseAPI):
    def __init__(self, client: APIClient):
        super().__init__(client)

    def welltypes(self) -> SummaryList:
        path: str = self._get_path("/welltypes")
        response: Response = self.client.get(url_path=path)
        welltypes_labels: LabelItems = LabelItems.parse_raw(response.text)
        welltypes: List[Label] = welltypes_labels.items
        return SummaryList(welltypes)
