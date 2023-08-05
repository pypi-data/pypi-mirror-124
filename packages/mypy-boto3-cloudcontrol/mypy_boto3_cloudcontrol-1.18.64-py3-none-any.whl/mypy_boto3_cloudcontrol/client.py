"""
Type annotations for cloudcontrol service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_cloudcontrol import CloudControlApiClient

    client: CloudControlApiClient = boto3.client("cloudcontrol")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CancelResourceRequestOutputTypeDef,
    CreateResourceOutputTypeDef,
    DeleteResourceOutputTypeDef,
    GetResourceOutputTypeDef,
    GetResourceRequestStatusOutputTypeDef,
    ListResourceRequestsOutputTypeDef,
    ListResourcesOutputTypeDef,
    ResourceRequestStatusFilterTypeDef,
    UpdateResourceOutputTypeDef,
)
from .waiter import ResourceRequestSuccessWaiter

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CloudControlApiClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientTokenConflictException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConcurrentOperationException: Type[BotocoreClientError]
    GeneralServiceException: Type[BotocoreClientError]
    HandlerFailureException: Type[BotocoreClientError]
    HandlerInternalFailureException: Type[BotocoreClientError]
    InvalidCredentialsException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    NetworkFailureException: Type[BotocoreClientError]
    NotStabilizedException: Type[BotocoreClientError]
    NotUpdatableException: Type[BotocoreClientError]
    PrivateTypeException: Type[BotocoreClientError]
    RequestTokenNotFoundException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceInternalErrorException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TypeNotFoundException: Type[BotocoreClientError]
    UnsupportedActionException: Type[BotocoreClientError]


class CloudControlApiClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudControlApiClient exceptions.
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html#can_paginate)
        """

    def cancel_resource_request(self, *, RequestToken: str) -> CancelResourceRequestOutputTypeDef:
        """
        Cancels the specified resource operation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client.cancel_resource_request)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html#cancel_resource_request)
        """

    def create_resource(
        self,
        *,
        TypeName: str,
        DesiredState: str,
        TypeVersionId: str = ...,
        RoleArn: str = ...,
        ClientToken: str = ...
    ) -> CreateResourceOutputTypeDef:
        """
        Creates the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client.create_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html#create_resource)
        """

    def delete_resource(
        self,
        *,
        TypeName: str,
        Identifier: str,
        TypeVersionId: str = ...,
        RoleArn: str = ...,
        ClientToken: str = ...
    ) -> DeleteResourceOutputTypeDef:
        """
        Deletes the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client.delete_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html#delete_resource)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html#generate_presigned_url)
        """

    def get_resource(
        self, *, TypeName: str, Identifier: str, TypeVersionId: str = ..., RoleArn: str = ...
    ) -> GetResourceOutputTypeDef:
        """
        Returns information about the current state of the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client.get_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html#get_resource)
        """

    def get_resource_request_status(
        self, *, RequestToken: str
    ) -> GetResourceRequestStatusOutputTypeDef:
        """
        Returns the current status of a resource operation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client.get_resource_request_status)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html#get_resource_request_status)
        """

    def list_resource_requests(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        ResourceRequestStatusFilter: "ResourceRequestStatusFilterTypeDef" = ...
    ) -> ListResourceRequestsOutputTypeDef:
        """
        Returns existing resource operation requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client.list_resource_requests)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html#list_resource_requests)
        """

    def list_resources(
        self,
        *,
        TypeName: str,
        TypeVersionId: str = ...,
        RoleArn: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ResourceModel: str = ...
    ) -> ListResourcesOutputTypeDef:
        """
        Returns information about the specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client.list_resources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html#list_resources)
        """

    def update_resource(
        self,
        *,
        TypeName: str,
        Identifier: str,
        PatchDocument: str,
        TypeVersionId: str = ...,
        RoleArn: str = ...,
        ClientToken: str = ...
    ) -> UpdateResourceOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Client.update_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/client.html#update_resource)
        """

    def get_waiter(
        self, waiter_name: Literal["resource_request_success"]
    ) -> ResourceRequestSuccessWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudcontrol.html#CloudControlApi.Waiter.ResourceRequestSuccess)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudcontrol/waiters.html#resourcerequestsuccesswaiter)
        """
