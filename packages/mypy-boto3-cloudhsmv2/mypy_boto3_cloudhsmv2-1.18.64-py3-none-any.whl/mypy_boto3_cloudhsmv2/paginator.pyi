"""
Type annotations for cloudhsmv2 service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_cloudhsmv2 import CloudHSMV2Client
    from mypy_boto3_cloudhsmv2.paginator import (
        DescribeBackupsPaginator,
        DescribeClustersPaginator,
        ListTagsPaginator,
    )

    client: CloudHSMV2Client = boto3.client("cloudhsmv2")

    describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
    describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
    list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```
"""
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeBackupsResponseTypeDef,
    DescribeClustersResponseTypeDef,
    ListTagsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("DescribeBackupsPaginator", "DescribeClustersPaginator", "ListTagsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeBackupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.DescribeBackups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators.html#describebackupspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Mapping[str, Sequence[str]] = ...,
        SortAscending: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeBackupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.DescribeBackups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators.html#describebackupspaginator)
        """

class DescribeClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.DescribeClusters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators.html#describeclusterspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Mapping[str, Sequence[str]] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.DescribeClusters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators.html#describeclusterspaginator)
        """

class ListTagsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.ListTags)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators.html#listtagspaginator)
    """

    def paginate(
        self, *, ResourceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.ListTags.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudhsmv2/paginators.html#listtagspaginator)
        """
