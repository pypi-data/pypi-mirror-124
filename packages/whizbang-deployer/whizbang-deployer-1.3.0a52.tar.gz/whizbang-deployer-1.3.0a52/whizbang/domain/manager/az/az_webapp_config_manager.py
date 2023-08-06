from whizbang.domain.manager.az.az_manager_base import AzManagerBase
from whizbang.domain.models.webapp_settings import WebappSettings
from whizbang.domain.repository.az.az_webapp_config_repository import AzWebappConfigRepository


class AzWebappConfigManager(AzManagerBase):
    def __init__(self, repository: AzWebappConfigRepository):
        AzManagerBase.__init__(self, repository)
        self._repository: AzWebappConfigRepository = repository

    def add_setting(self, settings: WebappSettings):
        return self._repository.create(settings=settings)
