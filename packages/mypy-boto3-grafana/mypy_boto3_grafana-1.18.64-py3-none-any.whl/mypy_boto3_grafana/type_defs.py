"""
Type annotations for grafana service type definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_grafana/type_defs.html)

Usage::

    ```python
    from mypy_boto3_grafana.type_defs import AssertionAttributesTypeDef

    data: AssertionAttributesTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Sequence

from .literals import (
    AccountAccessTypeType,
    AuthenticationProviderTypesType,
    DataSourceTypeType,
    LicenseTypeType,
    PermissionTypeType,
    RoleType,
    SamlConfigurationStatusType,
    UpdateActionType,
    UserTypeType,
    WorkspaceStatusType,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssertionAttributesTypeDef",
    "AssociateLicenseRequestRequestTypeDef",
    "AssociateLicenseResponseTypeDef",
    "AuthenticationDescriptionTypeDef",
    "AuthenticationSummaryTypeDef",
    "AwsSsoAuthenticationTypeDef",
    "CreateWorkspaceRequestRequestTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "DeleteWorkspaceRequestRequestTypeDef",
    "DeleteWorkspaceResponseTypeDef",
    "DescribeWorkspaceAuthenticationRequestRequestTypeDef",
    "DescribeWorkspaceAuthenticationResponseTypeDef",
    "DescribeWorkspaceRequestRequestTypeDef",
    "DescribeWorkspaceResponseTypeDef",
    "DisassociateLicenseRequestRequestTypeDef",
    "DisassociateLicenseResponseTypeDef",
    "IdpMetadataTypeDef",
    "ListPermissionsRequestRequestTypeDef",
    "ListPermissionsResponseTypeDef",
    "ListWorkspacesRequestRequestTypeDef",
    "ListWorkspacesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionEntryTypeDef",
    "ResponseMetadataTypeDef",
    "RoleValuesTypeDef",
    "SamlAuthenticationTypeDef",
    "SamlConfigurationTypeDef",
    "UpdateErrorTypeDef",
    "UpdateInstructionTypeDef",
    "UpdatePermissionsRequestRequestTypeDef",
    "UpdatePermissionsResponseTypeDef",
    "UpdateWorkspaceAuthenticationRequestRequestTypeDef",
    "UpdateWorkspaceAuthenticationResponseTypeDef",
    "UpdateWorkspaceRequestRequestTypeDef",
    "UpdateWorkspaceResponseTypeDef",
    "UserTypeDef",
    "WorkspaceDescriptionTypeDef",
    "WorkspaceSummaryTypeDef",
)

AssertionAttributesTypeDef = TypedDict(
    "AssertionAttributesTypeDef",
    {
        "email": str,
        "groups": str,
        "login": str,
        "name": str,
        "org": str,
        "role": str,
    },
    total=False,
)

AssociateLicenseRequestRequestTypeDef = TypedDict(
    "AssociateLicenseRequestRequestTypeDef",
    {
        "licenseType": LicenseTypeType,
        "workspaceId": str,
    },
)

AssociateLicenseResponseTypeDef = TypedDict(
    "AssociateLicenseResponseTypeDef",
    {
        "workspace": "WorkspaceDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredAuthenticationDescriptionTypeDef = TypedDict(
    "_RequiredAuthenticationDescriptionTypeDef",
    {
        "providers": List[AuthenticationProviderTypesType],
    },
)
_OptionalAuthenticationDescriptionTypeDef = TypedDict(
    "_OptionalAuthenticationDescriptionTypeDef",
    {
        "awsSso": "AwsSsoAuthenticationTypeDef",
        "saml": "SamlAuthenticationTypeDef",
    },
    total=False,
)


class AuthenticationDescriptionTypeDef(
    _RequiredAuthenticationDescriptionTypeDef, _OptionalAuthenticationDescriptionTypeDef
):
    pass


_RequiredAuthenticationSummaryTypeDef = TypedDict(
    "_RequiredAuthenticationSummaryTypeDef",
    {
        "providers": List[AuthenticationProviderTypesType],
    },
)
_OptionalAuthenticationSummaryTypeDef = TypedDict(
    "_OptionalAuthenticationSummaryTypeDef",
    {
        "samlConfigurationStatus": SamlConfigurationStatusType,
    },
    total=False,
)


class AuthenticationSummaryTypeDef(
    _RequiredAuthenticationSummaryTypeDef, _OptionalAuthenticationSummaryTypeDef
):
    pass


AwsSsoAuthenticationTypeDef = TypedDict(
    "AwsSsoAuthenticationTypeDef",
    {
        "ssoClientId": str,
    },
    total=False,
)

_RequiredCreateWorkspaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkspaceRequestRequestTypeDef",
    {
        "accountAccessType": AccountAccessTypeType,
        "authenticationProviders": Sequence[AuthenticationProviderTypesType],
        "permissionType": PermissionTypeType,
    },
)
_OptionalCreateWorkspaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkspaceRequestRequestTypeDef",
    {
        "clientToken": str,
        "organizationRoleName": str,
        "stackSetName": str,
        "workspaceDataSources": Sequence[DataSourceTypeType],
        "workspaceDescription": str,
        "workspaceName": str,
        "workspaceNotificationDestinations": Sequence[Literal["SNS"]],
        "workspaceOrganizationalUnits": Sequence[str],
        "workspaceRoleArn": str,
    },
    total=False,
)


class CreateWorkspaceRequestRequestTypeDef(
    _RequiredCreateWorkspaceRequestRequestTypeDef, _OptionalCreateWorkspaceRequestRequestTypeDef
):
    pass


CreateWorkspaceResponseTypeDef = TypedDict(
    "CreateWorkspaceResponseTypeDef",
    {
        "workspace": "WorkspaceDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteWorkspaceRequestRequestTypeDef = TypedDict(
    "DeleteWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

DeleteWorkspaceResponseTypeDef = TypedDict(
    "DeleteWorkspaceResponseTypeDef",
    {
        "workspace": "WorkspaceDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeWorkspaceAuthenticationRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceAuthenticationRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

DescribeWorkspaceAuthenticationResponseTypeDef = TypedDict(
    "DescribeWorkspaceAuthenticationResponseTypeDef",
    {
        "authentication": "AuthenticationDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeWorkspaceRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

DescribeWorkspaceResponseTypeDef = TypedDict(
    "DescribeWorkspaceResponseTypeDef",
    {
        "workspace": "WorkspaceDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisassociateLicenseRequestRequestTypeDef = TypedDict(
    "DisassociateLicenseRequestRequestTypeDef",
    {
        "licenseType": LicenseTypeType,
        "workspaceId": str,
    },
)

DisassociateLicenseResponseTypeDef = TypedDict(
    "DisassociateLicenseResponseTypeDef",
    {
        "workspace": "WorkspaceDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

IdpMetadataTypeDef = TypedDict(
    "IdpMetadataTypeDef",
    {
        "url": str,
        "xml": str,
    },
    total=False,
)

_RequiredListPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredListPermissionsRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalListPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalListPermissionsRequestRequestTypeDef",
    {
        "groupId": str,
        "maxResults": int,
        "nextToken": str,
        "userId": str,
        "userType": UserTypeType,
    },
    total=False,
)


class ListPermissionsRequestRequestTypeDef(
    _RequiredListPermissionsRequestRequestTypeDef, _OptionalListPermissionsRequestRequestTypeDef
):
    pass


ListPermissionsResponseTypeDef = TypedDict(
    "ListPermissionsResponseTypeDef",
    {
        "nextToken": str,
        "permissions": List["PermissionEntryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWorkspacesRequestRequestTypeDef = TypedDict(
    "ListWorkspacesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListWorkspacesResponseTypeDef = TypedDict(
    "ListWorkspacesResponseTypeDef",
    {
        "nextToken": str,
        "workspaces": List["WorkspaceSummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PermissionEntryTypeDef = TypedDict(
    "PermissionEntryTypeDef",
    {
        "role": RoleType,
        "user": "UserTypeDef",
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, Any],
        "RetryAttempts": int,
    },
)

RoleValuesTypeDef = TypedDict(
    "RoleValuesTypeDef",
    {
        "admin": List[str],
        "editor": List[str],
    },
    total=False,
)

_RequiredSamlAuthenticationTypeDef = TypedDict(
    "_RequiredSamlAuthenticationTypeDef",
    {
        "status": SamlConfigurationStatusType,
    },
)
_OptionalSamlAuthenticationTypeDef = TypedDict(
    "_OptionalSamlAuthenticationTypeDef",
    {
        "configuration": "SamlConfigurationTypeDef",
    },
    total=False,
)


class SamlAuthenticationTypeDef(
    _RequiredSamlAuthenticationTypeDef, _OptionalSamlAuthenticationTypeDef
):
    pass


_RequiredSamlConfigurationTypeDef = TypedDict(
    "_RequiredSamlConfigurationTypeDef",
    {
        "idpMetadata": "IdpMetadataTypeDef",
    },
)
_OptionalSamlConfigurationTypeDef = TypedDict(
    "_OptionalSamlConfigurationTypeDef",
    {
        "allowedOrganizations": List[str],
        "assertionAttributes": "AssertionAttributesTypeDef",
        "loginValidityDuration": int,
        "roleValues": "RoleValuesTypeDef",
    },
    total=False,
)


class SamlConfigurationTypeDef(
    _RequiredSamlConfigurationTypeDef, _OptionalSamlConfigurationTypeDef
):
    pass


UpdateErrorTypeDef = TypedDict(
    "UpdateErrorTypeDef",
    {
        "causedBy": "UpdateInstructionTypeDef",
        "code": int,
        "message": str,
    },
)

UpdateInstructionTypeDef = TypedDict(
    "UpdateInstructionTypeDef",
    {
        "action": UpdateActionType,
        "role": RoleType,
        "users": Sequence["UserTypeDef"],
    },
)

UpdatePermissionsRequestRequestTypeDef = TypedDict(
    "UpdatePermissionsRequestRequestTypeDef",
    {
        "updateInstructionBatch": Sequence["UpdateInstructionTypeDef"],
        "workspaceId": str,
    },
)

UpdatePermissionsResponseTypeDef = TypedDict(
    "UpdatePermissionsResponseTypeDef",
    {
        "errors": List["UpdateErrorTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateWorkspaceAuthenticationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkspaceAuthenticationRequestRequestTypeDef",
    {
        "authenticationProviders": Sequence[AuthenticationProviderTypesType],
        "workspaceId": str,
    },
)
_OptionalUpdateWorkspaceAuthenticationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkspaceAuthenticationRequestRequestTypeDef",
    {
        "samlConfiguration": "SamlConfigurationTypeDef",
    },
    total=False,
)


class UpdateWorkspaceAuthenticationRequestRequestTypeDef(
    _RequiredUpdateWorkspaceAuthenticationRequestRequestTypeDef,
    _OptionalUpdateWorkspaceAuthenticationRequestRequestTypeDef,
):
    pass


UpdateWorkspaceAuthenticationResponseTypeDef = TypedDict(
    "UpdateWorkspaceAuthenticationResponseTypeDef",
    {
        "authentication": "AuthenticationDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateWorkspaceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
_OptionalUpdateWorkspaceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkspaceRequestRequestTypeDef",
    {
        "accountAccessType": AccountAccessTypeType,
        "organizationRoleName": str,
        "permissionType": PermissionTypeType,
        "stackSetName": str,
        "workspaceDataSources": Sequence[DataSourceTypeType],
        "workspaceDescription": str,
        "workspaceName": str,
        "workspaceNotificationDestinations": Sequence[Literal["SNS"]],
        "workspaceOrganizationalUnits": Sequence[str],
        "workspaceRoleArn": str,
    },
    total=False,
)


class UpdateWorkspaceRequestRequestTypeDef(
    _RequiredUpdateWorkspaceRequestRequestTypeDef, _OptionalUpdateWorkspaceRequestRequestTypeDef
):
    pass


UpdateWorkspaceResponseTypeDef = TypedDict(
    "UpdateWorkspaceResponseTypeDef",
    {
        "workspace": "WorkspaceDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "id": str,
        "type": UserTypeType,
    },
)

_RequiredWorkspaceDescriptionTypeDef = TypedDict(
    "_RequiredWorkspaceDescriptionTypeDef",
    {
        "authentication": "AuthenticationSummaryTypeDef",
        "created": datetime,
        "dataSources": List[DataSourceTypeType],
        "endpoint": str,
        "grafanaVersion": str,
        "id": str,
        "modified": datetime,
        "status": WorkspaceStatusType,
    },
)
_OptionalWorkspaceDescriptionTypeDef = TypedDict(
    "_OptionalWorkspaceDescriptionTypeDef",
    {
        "accountAccessType": AccountAccessTypeType,
        "description": str,
        "freeTrialConsumed": bool,
        "freeTrialExpiration": datetime,
        "licenseExpiration": datetime,
        "licenseType": LicenseTypeType,
        "name": str,
        "notificationDestinations": List[Literal["SNS"]],
        "organizationRoleName": str,
        "organizationalUnits": List[str],
        "permissionType": PermissionTypeType,
        "stackSetName": str,
        "workspaceRoleArn": str,
    },
    total=False,
)


class WorkspaceDescriptionTypeDef(
    _RequiredWorkspaceDescriptionTypeDef, _OptionalWorkspaceDescriptionTypeDef
):
    pass


_RequiredWorkspaceSummaryTypeDef = TypedDict(
    "_RequiredWorkspaceSummaryTypeDef",
    {
        "authentication": "AuthenticationSummaryTypeDef",
        "created": datetime,
        "endpoint": str,
        "grafanaVersion": str,
        "id": str,
        "modified": datetime,
        "status": WorkspaceStatusType,
    },
)
_OptionalWorkspaceSummaryTypeDef = TypedDict(
    "_OptionalWorkspaceSummaryTypeDef",
    {
        "description": str,
        "name": str,
        "notificationDestinations": List[Literal["SNS"]],
    },
    total=False,
)


class WorkspaceSummaryTypeDef(_RequiredWorkspaceSummaryTypeDef, _OptionalWorkspaceSummaryTypeDef):
    pass
