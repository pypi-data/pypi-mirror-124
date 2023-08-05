"""
Type annotations for personalize-runtime service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_personalize_runtime import PersonalizeRuntimeClient

    client: PersonalizeRuntimeClient = boto3.client("personalize-runtime")
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import GetPersonalizedRankingResponseTypeDef, GetRecommendationsResponseTypeDef

__all__ = ("PersonalizeRuntimeClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class PersonalizeRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/personalize-runtime.html#PersonalizeRuntime.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client.html)
    """

    meta: ClientMeta
    @property
    def exceptions(self) -> Exceptions:
        """
        PersonalizeRuntimeClient exceptions.
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client.html#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client.html#generate_presigned_url)
        """
    def get_personalized_ranking(
        self,
        *,
        campaignArn: str,
        inputList: Sequence[str],
        userId: str,
        context: Mapping[str, str] = ...,
        filterArn: str = ...,
        filterValues: Mapping[str, str] = ...
    ) -> GetPersonalizedRankingResponseTypeDef:
        """
        Re-ranks a list of recommended items for the given user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.get_personalized_ranking)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client.html#get_personalized_ranking)
        """
    def get_recommendations(
        self,
        *,
        campaignArn: str,
        itemId: str = ...,
        userId: str = ...,
        numResults: int = ...,
        context: Mapping[str, str] = ...,
        filterArn: str = ...,
        filterValues: Mapping[str, str] = ...
    ) -> GetRecommendationsResponseTypeDef:
        """
        Returns a list of recommended items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/personalize-runtime.html#PersonalizeRuntime.Client.get_recommendations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_runtime/client.html#get_recommendations)
        """
