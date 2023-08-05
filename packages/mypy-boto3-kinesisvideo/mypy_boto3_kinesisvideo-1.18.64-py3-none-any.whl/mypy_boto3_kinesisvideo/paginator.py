"""
Type annotations for kinesisvideo service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_kinesisvideo import KinesisVideoClient
    from mypy_boto3_kinesisvideo.paginator import (
        ListSignalingChannelsPaginator,
        ListStreamsPaginator,
    )

    client: KinesisVideoClient = boto3.client("kinesisvideo")

    list_signaling_channels_paginator: ListSignalingChannelsPaginator = client.get_paginator("list_signaling_channels")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ChannelNameConditionTypeDef,
    ListSignalingChannelsOutputTypeDef,
    ListStreamsOutputTypeDef,
    PaginatorConfigTypeDef,
    StreamNameConditionTypeDef,
)

__all__ = ("ListSignalingChannelsPaginator", "ListStreamsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListSignalingChannelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/kinesisvideo.html#KinesisVideo.Paginator.ListSignalingChannels)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators.html#listsignalingchannelspaginator)
    """

    def paginate(
        self,
        *,
        ChannelNameCondition: "ChannelNameConditionTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSignalingChannelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/kinesisvideo.html#KinesisVideo.Paginator.ListSignalingChannels.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators.html#listsignalingchannelspaginator)
        """


class ListStreamsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/kinesisvideo.html#KinesisVideo.Paginator.ListStreams)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators.html#liststreamspaginator)
    """

    def paginate(
        self,
        *,
        StreamNameCondition: "StreamNameConditionTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStreamsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/kinesisvideo.html#KinesisVideo.Paginator.ListStreams.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_kinesisvideo/paginators.html#liststreamspaginator)
        """
