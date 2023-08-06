from whizbang.data.az_cli_context import AzCliContext
from whizbang.domain.models.webapp_settings import WebappSettings
from whizbang.domain.repository.az.az_repository_base import AzRepositoryBase


class AzWebappConfigRepository(AzRepositoryBase):
    def __init__(self, context: AzCliContext):
        AzRepositoryBase.__init__(self, context)

    @property
    def _resource_provider(self) -> str: return 'webapp config'

    def create(self, settings: WebappSettings):
        result = self._execute(f'appsettings set --resource-group {settings.resource_group}'
                               f' --name {settings.webapp_name}'
                               f' --settings {settings.setting_key}={settings.setting_value}')
        return result
