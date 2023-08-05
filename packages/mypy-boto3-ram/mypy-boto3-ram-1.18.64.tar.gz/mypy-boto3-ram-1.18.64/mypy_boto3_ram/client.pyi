"""
Type annotations for ram service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_ram import RAMClient

    client: RAMClient = boto3.client("ram")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    ResourceOwnerType,
    ResourceShareAssociationStatusType,
    ResourceShareAssociationTypeType,
    ResourceShareStatusType,
)
from .paginator import (
    GetResourcePoliciesPaginator,
    GetResourceShareAssociationsPaginator,
    GetResourceShareInvitationsPaginator,
    GetResourceSharesPaginator,
    ListPrincipalsPaginator,
    ListResourcesPaginator,
)
from .type_defs import (
    AcceptResourceShareInvitationResponseTypeDef,
    AssociateResourceSharePermissionResponseTypeDef,
    AssociateResourceShareResponseTypeDef,
    CreateResourceShareResponseTypeDef,
    DeleteResourceShareResponseTypeDef,
    DisassociateResourceSharePermissionResponseTypeDef,
    DisassociateResourceShareResponseTypeDef,
    EnableSharingWithAwsOrganizationResponseTypeDef,
    GetPermissionResponseTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetResourceShareAssociationsResponseTypeDef,
    GetResourceShareInvitationsResponseTypeDef,
    GetResourceSharesResponseTypeDef,
    ListPendingInvitationResourcesResponseTypeDef,
    ListPermissionsResponseTypeDef,
    ListPrincipalsResponseTypeDef,
    ListResourceSharePermissionsResponseTypeDef,
    ListResourcesResponseTypeDef,
    ListResourceTypesResponseTypeDef,
    PromoteResourceShareCreatedFromPolicyResponseTypeDef,
    RejectResourceShareInvitationResponseTypeDef,
    TagFilterTypeDef,
    TagTypeDef,
    UpdateResourceShareResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("RAMClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InvalidClientTokenException: Type[BotocoreClientError]
    InvalidMaxResultsException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidResourceTypeException: Type[BotocoreClientError]
    InvalidStateTransitionException: Type[BotocoreClientError]
    MalformedArnException: Type[BotocoreClientError]
    MissingRequiredParameterException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    ResourceArnNotFoundException: Type[BotocoreClientError]
    ResourceShareInvitationAlreadyAcceptedException: Type[BotocoreClientError]
    ResourceShareInvitationAlreadyRejectedException: Type[BotocoreClientError]
    ResourceShareInvitationArnNotFoundException: Type[BotocoreClientError]
    ResourceShareInvitationExpiredException: Type[BotocoreClientError]
    ResourceShareLimitExceededException: Type[BotocoreClientError]
    ServerInternalException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TagLimitExceededException: Type[BotocoreClientError]
    TagPolicyViolationException: Type[BotocoreClientError]
    UnknownResourceException: Type[BotocoreClientError]

class RAMClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html)
    """

    meta: ClientMeta
    @property
    def exceptions(self) -> Exceptions:
        """
        RAMClient exceptions.
        """
    def accept_resource_share_invitation(
        self, *, resourceShareInvitationArn: str, clientToken: str = ...
    ) -> AcceptResourceShareInvitationResponseTypeDef:
        """
        Accepts an invitation to a resource share from another Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.accept_resource_share_invitation)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#accept_resource_share_invitation)
        """
    def associate_resource_share(
        self,
        *,
        resourceShareArn: str,
        resourceArns: Sequence[str] = ...,
        principals: Sequence[str] = ...,
        clientToken: str = ...
    ) -> AssociateResourceShareResponseTypeDef:
        """
        Associates the specified resource share with the specified principals and
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.associate_resource_share)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#associate_resource_share)
        """
    def associate_resource_share_permission(
        self,
        *,
        resourceShareArn: str,
        permissionArn: str,
        replace: bool = ...,
        clientToken: str = ...,
        permissionVersion: int = ...
    ) -> AssociateResourceSharePermissionResponseTypeDef:
        """
        Associates a permission with a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.associate_resource_share_permission)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#associate_resource_share_permission)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#can_paginate)
        """
    def create_resource_share(
        self,
        *,
        name: str,
        resourceArns: Sequence[str] = ...,
        principals: Sequence[str] = ...,
        tags: Sequence["TagTypeDef"] = ...,
        allowExternalPrincipals: bool = ...,
        clientToken: str = ...,
        permissionArns: Sequence[str] = ...
    ) -> CreateResourceShareResponseTypeDef:
        """
        Creates a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.create_resource_share)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#create_resource_share)
        """
    def delete_resource_share(
        self, *, resourceShareArn: str, clientToken: str = ...
    ) -> DeleteResourceShareResponseTypeDef:
        """
        Deletes the specified resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.delete_resource_share)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#delete_resource_share)
        """
    def disassociate_resource_share(
        self,
        *,
        resourceShareArn: str,
        resourceArns: Sequence[str] = ...,
        principals: Sequence[str] = ...,
        clientToken: str = ...
    ) -> DisassociateResourceShareResponseTypeDef:
        """
        Disassociates the specified principals or resources from the specified resource
        share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.disassociate_resource_share)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#disassociate_resource_share)
        """
    def disassociate_resource_share_permission(
        self, *, resourceShareArn: str, permissionArn: str, clientToken: str = ...
    ) -> DisassociateResourceSharePermissionResponseTypeDef:
        """
        Disassociates an RAM permission from a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.disassociate_resource_share_permission)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#disassociate_resource_share_permission)
        """
    def enable_sharing_with_aws_organization(
        self,
    ) -> EnableSharingWithAwsOrganizationResponseTypeDef:
        """
        Enables resource sharing within your organization in Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.enable_sharing_with_aws_organization)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#enable_sharing_with_aws_organization)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#generate_presigned_url)
        """
    def get_permission(
        self, *, permissionArn: str, permissionVersion: int = ...
    ) -> GetPermissionResponseTypeDef:
        """
        Gets the contents of an RAM permission in JSON format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.get_permission)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#get_permission)
        """
    def get_resource_policies(
        self,
        *,
        resourceArns: Sequence[str],
        principal: str = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> GetResourcePoliciesResponseTypeDef:
        """
        Gets the policies for the specified resources that you own and have shared.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.get_resource_policies)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#get_resource_policies)
        """
    def get_resource_share_associations(
        self,
        *,
        associationType: ResourceShareAssociationTypeType,
        resourceShareArns: Sequence[str] = ...,
        resourceArn: str = ...,
        principal: str = ...,
        associationStatus: ResourceShareAssociationStatusType = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> GetResourceShareAssociationsResponseTypeDef:
        """
        Gets the resources or principals for the resource shares that you own.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.get_resource_share_associations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#get_resource_share_associations)
        """
    def get_resource_share_invitations(
        self,
        *,
        resourceShareInvitationArns: Sequence[str] = ...,
        resourceShareArns: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> GetResourceShareInvitationsResponseTypeDef:
        """
        Gets the invitations that you have received for resource shares.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.get_resource_share_invitations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#get_resource_share_invitations)
        """
    def get_resource_shares(
        self,
        *,
        resourceOwner: ResourceOwnerType,
        resourceShareArns: Sequence[str] = ...,
        resourceShareStatus: ResourceShareStatusType = ...,
        name: str = ...,
        tagFilters: Sequence["TagFilterTypeDef"] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        permissionArn: str = ...
    ) -> GetResourceSharesResponseTypeDef:
        """
        Gets the resource shares that you own or the resource shares that are shared
        with you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.get_resource_shares)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#get_resource_shares)
        """
    def list_pending_invitation_resources(
        self, *, resourceShareInvitationArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListPendingInvitationResourcesResponseTypeDef:
        """
        Lists the resources in a resource share that is shared with you but that the
        invitation is still pending for.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.list_pending_invitation_resources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#list_pending_invitation_resources)
        """
    def list_permissions(
        self, *, resourceType: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListPermissionsResponseTypeDef:
        """
        Lists the RAM permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.list_permissions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#list_permissions)
        """
    def list_principals(
        self,
        *,
        resourceOwner: ResourceOwnerType,
        resourceArn: str = ...,
        principals: Sequence[str] = ...,
        resourceType: str = ...,
        resourceShareArns: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListPrincipalsResponseTypeDef:
        """
        Lists the principals that you have shared resources with or that have shared
        resources with you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.list_principals)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#list_principals)
        """
    def list_resource_share_permissions(
        self, *, resourceShareArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListResourceSharePermissionsResponseTypeDef:
        """
        Lists the RAM permissions that are associated with a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.list_resource_share_permissions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#list_resource_share_permissions)
        """
    def list_resource_types(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListResourceTypesResponseTypeDef:
        """
        Lists the shareable resource types supported by RAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.list_resource_types)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#list_resource_types)
        """
    def list_resources(
        self,
        *,
        resourceOwner: ResourceOwnerType,
        principal: str = ...,
        resourceType: str = ...,
        resourceArns: Sequence[str] = ...,
        resourceShareArns: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListResourcesResponseTypeDef:
        """
        Lists the resources that you added to a resource shares or the resources that
        are shared with you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.list_resources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#list_resources)
        """
    def promote_resource_share_created_from_policy(
        self, *, resourceShareArn: str
    ) -> PromoteResourceShareCreatedFromPolicyResponseTypeDef:
        """
        Resource shares that were created by attaching a policy to a resource are
        visible only to the resource share owner, and the resource share cannot be
        modified in RAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.promote_resource_share_created_from_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#promote_resource_share_created_from_policy)
        """
    def reject_resource_share_invitation(
        self, *, resourceShareInvitationArn: str, clientToken: str = ...
    ) -> RejectResourceShareInvitationResponseTypeDef:
        """
        Rejects an invitation to a resource share from another Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.reject_resource_share_invitation)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#reject_resource_share_invitation)
        """
    def tag_resource(
        self, *, resourceShareArn: str, tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource share that you own.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#tag_resource)
        """
    def untag_resource(self, *, resourceShareArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource share that you own.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#untag_resource)
        """
    def update_resource_share(
        self,
        *,
        resourceShareArn: str,
        name: str = ...,
        allowExternalPrincipals: bool = ...,
        clientToken: str = ...
    ) -> UpdateResourceShareResponseTypeDef:
        """
        Updates the specified resource share that you own.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Client.update_resource_share)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/client.html#update_resource_share)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_policies"]
    ) -> GetResourcePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Paginator.GetResourcePolicies)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators.html#getresourcepoliciespaginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_share_associations"]
    ) -> GetResourceShareAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Paginator.GetResourceShareAssociations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators.html#getresourceshareassociationspaginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_share_invitations"]
    ) -> GetResourceShareInvitationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Paginator.GetResourceShareInvitations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators.html#getresourceshareinvitationspaginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_shares"]
    ) -> GetResourceSharesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Paginator.GetResourceShares)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators.html#getresourcesharespaginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_principals"]) -> ListPrincipalsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Paginator.ListPrincipals)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators.html#listprincipalspaginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_resources"]) -> ListResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ram.html#RAM.Paginator.ListResources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ram/paginators.html#listresourcespaginator)
        """
