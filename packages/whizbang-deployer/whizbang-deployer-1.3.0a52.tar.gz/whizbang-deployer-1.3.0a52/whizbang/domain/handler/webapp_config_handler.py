from whizbang.config.app_config import AppConfig
from whizbang.domain.handler.handler_base import HandlerBase
from whizbang.domain.manager.az.az_webapp_config_manager import AzWebappConfigManager
from whizbang.domain.models.webapp_settings import WebappSettings


class WebappConfigHandler(HandlerBase):
    def __init__(self, app_config: AppConfig, manager: AzWebappConfigManager):
        HandlerBase.__init__(self, app_config=app_config)
        self.manager = manager

    def add_setting(self, setting_key: str, setting_value: str, resource_group: str, webapp_name: str):
        webapp_settings = WebappSettings(resource_group=resource_group,
                                         webapp_name=webapp_name,
                                         setting_key=setting_key,
                                         setting_value=setting_value)
        return self.manager.add_setting(settings=webapp_settings)
