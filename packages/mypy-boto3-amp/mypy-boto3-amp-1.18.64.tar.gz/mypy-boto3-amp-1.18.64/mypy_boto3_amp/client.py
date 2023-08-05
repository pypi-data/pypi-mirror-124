"""
Type annotations for amp service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_amp import PrometheusServiceClient

    client: PrometheusServiceClient = boto3.client("amp")
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .paginator import ListRuleGroupsNamespacesPaginator, ListWorkspacesPaginator
from .type_defs import (
    CreateAlertManagerDefinitionResponseTypeDef,
    CreateRuleGroupsNamespaceResponseTypeDef,
    CreateWorkspaceResponseTypeDef,
    DescribeAlertManagerDefinitionResponseTypeDef,
    DescribeRuleGroupsNamespaceResponseTypeDef,
    DescribeWorkspaceResponseTypeDef,
    ListRuleGroupsNamespacesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkspacesResponseTypeDef,
    PutAlertManagerDefinitionResponseTypeDef,
    PutRuleGroupsNamespaceResponseTypeDef,
)
from .waiter import WorkspaceActiveWaiter, WorkspaceDeletedWaiter

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("PrometheusServiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class PrometheusServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PrometheusServiceClient exceptions.
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#can_paginate)
        """

    def create_alert_manager_definition(
        self,
        *,
        data: Union[bytes, IO[bytes], StreamingBody],
        workspaceId: str,
        clientToken: str = ...
    ) -> CreateAlertManagerDefinitionResponseTypeDef:
        """
        Create an alert manager definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.create_alert_manager_definition)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#create_alert_manager_definition)
        """

    def create_rule_groups_namespace(
        self,
        *,
        data: Union[bytes, IO[bytes], StreamingBody],
        name: str,
        workspaceId: str,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateRuleGroupsNamespaceResponseTypeDef:
        """
        Create a rule group namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.create_rule_groups_namespace)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#create_rule_groups_namespace)
        """

    def create_workspace(
        self, *, alias: str = ..., clientToken: str = ..., tags: Mapping[str, str] = ...
    ) -> CreateWorkspaceResponseTypeDef:
        """
        Creates a new AMP workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.create_workspace)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#create_workspace)
        """

    def delete_alert_manager_definition(self, *, workspaceId: str, clientToken: str = ...) -> None:
        """
        Deletes an alert manager definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.delete_alert_manager_definition)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#delete_alert_manager_definition)
        """

    def delete_rule_groups_namespace(
        self, *, name: str, workspaceId: str, clientToken: str = ...
    ) -> None:
        """
        Delete a rule groups namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.delete_rule_groups_namespace)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#delete_rule_groups_namespace)
        """

    def delete_workspace(self, *, workspaceId: str, clientToken: str = ...) -> None:
        """
        Deletes an AMP workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.delete_workspace)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#delete_workspace)
        """

    def describe_alert_manager_definition(
        self, *, workspaceId: str
    ) -> DescribeAlertManagerDefinitionResponseTypeDef:
        """
        Describes an alert manager definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.describe_alert_manager_definition)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#describe_alert_manager_definition)
        """

    def describe_rule_groups_namespace(
        self, *, name: str, workspaceId: str
    ) -> DescribeRuleGroupsNamespaceResponseTypeDef:
        """
        Describe a rule groups namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.describe_rule_groups_namespace)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#describe_rule_groups_namespace)
        """

    def describe_workspace(self, *, workspaceId: str) -> DescribeWorkspaceResponseTypeDef:
        """
        Describes an existing AMP workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.describe_workspace)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#describe_workspace)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#generate_presigned_url)
        """

    def list_rule_groups_namespaces(
        self, *, workspaceId: str, maxResults: int = ..., name: str = ..., nextToken: str = ...
    ) -> ListRuleGroupsNamespacesResponseTypeDef:
        """
        Lists rule groups namespaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.list_rule_groups_namespaces)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#list_rule_groups_namespaces)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags you have assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#list_tags_for_resource)
        """

    def list_workspaces(
        self, *, alias: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkspacesResponseTypeDef:
        """
        Lists all AMP workspaces, including workspaces being created or deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.list_workspaces)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#list_workspaces)
        """

    def put_alert_manager_definition(
        self,
        *,
        data: Union[bytes, IO[bytes], StreamingBody],
        workspaceId: str,
        clientToken: str = ...
    ) -> PutAlertManagerDefinitionResponseTypeDef:
        """
        Update an alert manager definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.put_alert_manager_definition)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#put_alert_manager_definition)
        """

    def put_rule_groups_namespace(
        self,
        *,
        data: Union[bytes, IO[bytes], StreamingBody],
        name: str,
        workspaceId: str,
        clientToken: str = ...
    ) -> PutRuleGroupsNamespaceResponseTypeDef:
        """
        Update a rule groups namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.put_rule_groups_namespace)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#put_rule_groups_namespace)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Creates tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#untag_resource)
        """

    def update_workspace_alias(
        self, *, workspaceId: str, alias: str = ..., clientToken: str = ...
    ) -> None:
        """
        Updates an AMP workspace alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Client.update_workspace_alias)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/client.html#update_workspace_alias)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_rule_groups_namespaces"]
    ) -> ListRuleGroupsNamespacesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Paginator.ListRuleGroupsNamespaces)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/paginators.html#listrulegroupsnamespacespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workspaces"]) -> ListWorkspacesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Paginator.ListWorkspaces)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/paginators.html#listworkspacespaginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["workspace_active"]) -> WorkspaceActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Waiter.WorkspaceActive)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/waiters.html#workspaceactivewaiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["workspace_deleted"]) -> WorkspaceDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/amp.html#PrometheusService.Waiter.WorkspaceDeleted)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_amp/waiters.html#workspacedeletedwaiter)
        """
