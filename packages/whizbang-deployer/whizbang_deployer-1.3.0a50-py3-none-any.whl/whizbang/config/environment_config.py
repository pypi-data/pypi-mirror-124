from typing import List, Optional

from pydantic import BaseModel

from whizbang.domain.models.keyvault.keyvault_access_policy import KeyVaultAccessPolicy
from whizbang.domain.models.rbac_policy import RBACPolicy


class EnvironmentConfig(BaseModel):
    subscription_id: str
    tenant_id: str
    resource_group_name: str
    resource_group_location: str
    resource_name_prefix: str
    resource_name_suffix: str
    environment: str

    # todo: remove
    vnet_address_prefix: str

    # nested
    rbac_policies: Optional[List[RBACPolicy]] = []
    keyvault_access_policies: Optional[List[KeyVaultAccessPolicy]] = []
