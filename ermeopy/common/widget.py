from ..const import API_ERMEO_WIDGET_URL
from ..ermeo import ErmeoV1
from ..resource import Resource
from ..schema.widget_schema import WidgetSchema, WidgetSchemaUpdate


class Widget(Resource):
    """
    @param ermeo_v1: ErmeoV1
    """

    def __init__(self, ermeo_v1: ErmeoV1):
        self.ermeo_v1 = ermeo_v1
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_WIDGET_URL, WidgetSchema,
                         WidgetSchemaUpdate)

    def search(self, search_dict: dict, raw: bool = False):
        raise NotImplementedError

    def delete(self, search_dict: dict, raw: bool = False):
        raise NotImplementedError
