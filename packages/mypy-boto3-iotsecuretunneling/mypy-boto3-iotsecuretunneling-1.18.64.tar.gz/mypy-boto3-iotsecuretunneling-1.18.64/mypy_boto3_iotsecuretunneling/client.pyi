"""
Type annotations for iotsecuretunneling service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_iotsecuretunneling import IoTSecureTunnelingClient

    client: IoTSecureTunnelingClient = boto3.client("iotsecuretunneling")
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    DescribeTunnelResponseTypeDef,
    DestinationConfigTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTunnelsResponseTypeDef,
    OpenTunnelResponseTypeDef,
    TagTypeDef,
    TimeoutConfigTypeDef,
)

__all__ = ("IoTSecureTunnelingClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class IoTSecureTunnelingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html)
    """

    meta: ClientMeta
    @property
    def exceptions(self) -> Exceptions:
        """
        IoTSecureTunnelingClient exceptions.
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html#can_paginate)
        """
    def close_tunnel(self, *, tunnelId: str, delete: bool = ...) -> Dict[str, Any]:
        """
        Closes a tunnel identified by the unique tunnel id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.close_tunnel)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html#close_tunnel)
        """
    def describe_tunnel(self, *, tunnelId: str) -> DescribeTunnelResponseTypeDef:
        """
        Gets information about a tunnel identified by the unique tunnel id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.describe_tunnel)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html#describe_tunnel)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html#generate_presigned_url)
        """
    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html#list_tags_for_resource)
        """
    def list_tunnels(
        self, *, thingName: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListTunnelsResponseTypeDef:
        """
        List all tunnels for an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.list_tunnels)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html#list_tunnels)
        """
    def open_tunnel(
        self,
        *,
        description: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        destinationConfig: "DestinationConfigTypeDef" = ...,
        timeoutConfig: "TimeoutConfigTypeDef" = ...
    ) -> OpenTunnelResponseTypeDef:
        """
        Creates a new tunnel, and returns two client access tokens for clients to use to
        connect to the AWS IoT Secure Tunneling proxy server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.open_tunnel)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html#open_tunnel)
        """
    def tag_resource(self, *, resourceArn: str, tags: Sequence["TagTypeDef"]) -> Dict[str, Any]:
        """
        A resource tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html#tag_resource)
        """
    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client.html#untag_resource)
        """
