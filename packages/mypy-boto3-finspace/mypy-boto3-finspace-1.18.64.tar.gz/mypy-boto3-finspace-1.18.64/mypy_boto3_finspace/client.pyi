"""
Type annotations for finspace service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_finspace import finspaceClient

    client: finspaceClient = boto3.client("finspace")
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import FederationModeType
from .type_defs import (
    CreateEnvironmentResponseTypeDef,
    FederationParametersTypeDef,
    GetEnvironmentResponseTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    UpdateEnvironmentResponseTypeDef,
)

__all__ = ("finspaceClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class finspaceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html)
    """

    meta: ClientMeta
    @property
    def exceptions(self) -> Exceptions:
        """
        finspaceClient exceptions.
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html#can_paginate)
        """
    def create_environment(
        self,
        *,
        name: str,
        description: str = ...,
        kmsKeyId: str = ...,
        tags: Mapping[str, str] = ...,
        federationMode: FederationModeType = ...,
        federationParameters: "FederationParametersTypeDef" = ...
    ) -> CreateEnvironmentResponseTypeDef:
        """
        Create a new FinSpace environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client.create_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html#create_environment)
        """
    def delete_environment(self, *, environmentId: str) -> Dict[str, Any]:
        """
        Delete an FinSpace environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client.delete_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html#delete_environment)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html#generate_presigned_url)
        """
    def get_environment(self, *, environmentId: str) -> GetEnvironmentResponseTypeDef:
        """
        Returns the FinSpace environment object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client.get_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html#get_environment)
        """
    def list_environments(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListEnvironmentsResponseTypeDef:
        """
        A list of all of your FinSpace environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client.list_environments)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html#list_environments)
        """
    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        A list of all tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html#list_tags_for_resource)
        """
    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds metadata tags to a FinSpace resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html#tag_resource)
        """
    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes metadata tags from a FinSpace resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html#untag_resource)
        """
    def update_environment(
        self,
        *,
        environmentId: str,
        name: str = ...,
        description: str = ...,
        federationMode: FederationModeType = ...,
        federationParameters: "FederationParametersTypeDef" = ...
    ) -> UpdateEnvironmentResponseTypeDef:
        """
        Update your FinSpace environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/finspace.html#finspace.Client.update_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_finspace/client.html#update_environment)
        """
