"""
Type annotations for ecr service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_ecr import ECRClient
    from mypy_boto3_ecr.paginator import (
        DescribeImageScanFindingsPaginator,
        DescribeImagesPaginator,
        DescribeRepositoriesPaginator,
        GetLifecyclePolicyPreviewPaginator,
        ListImagesPaginator,
    )

    client: ECRClient = boto3.client("ecr")

    describe_image_scan_findings_paginator: DescribeImageScanFindingsPaginator = client.get_paginator("describe_image_scan_findings")
    describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
    describe_repositories_paginator: DescribeRepositoriesPaginator = client.get_paginator("describe_repositories")
    get_lifecycle_policy_preview_paginator: GetLifecyclePolicyPreviewPaginator = client.get_paginator("get_lifecycle_policy_preview")
    list_images_paginator: ListImagesPaginator = client.get_paginator("list_images")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeImageScanFindingsResponseTypeDef,
    DescribeImagesFilterTypeDef,
    DescribeImagesResponseTypeDef,
    DescribeRepositoriesResponseTypeDef,
    GetLifecyclePolicyPreviewResponseTypeDef,
    ImageIdentifierTypeDef,
    LifecyclePolicyPreviewFilterTypeDef,
    ListImagesFilterTypeDef,
    ListImagesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeImageScanFindingsPaginator",
    "DescribeImagesPaginator",
    "DescribeRepositoriesPaginator",
    "GetLifecyclePolicyPreviewPaginator",
    "ListImagesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeImageScanFindingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ecr.html#ECR.Paginator.DescribeImageScanFindings)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html#describeimagescanfindingspaginator)
    """

    def paginate(
        self,
        *,
        repositoryName: str,
        imageId: "ImageIdentifierTypeDef",
        registryId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeImageScanFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ecr.html#ECR.Paginator.DescribeImageScanFindings.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html#describeimagescanfindingspaginator)
        """

class DescribeImagesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ecr.html#ECR.Paginator.DescribeImages)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html#describeimagespaginator)
    """

    def paginate(
        self,
        *,
        repositoryName: str,
        registryId: str = ...,
        imageIds: Sequence["ImageIdentifierTypeDef"] = ...,
        filter: "DescribeImagesFilterTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ecr.html#ECR.Paginator.DescribeImages.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html#describeimagespaginator)
        """

class DescribeRepositoriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ecr.html#ECR.Paginator.DescribeRepositories)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html#describerepositoriespaginator)
    """

    def paginate(
        self,
        *,
        registryId: str = ...,
        repositoryNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeRepositoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ecr.html#ECR.Paginator.DescribeRepositories.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html#describerepositoriespaginator)
        """

class GetLifecyclePolicyPreviewPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ecr.html#ECR.Paginator.GetLifecyclePolicyPreview)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html#getlifecyclepolicypreviewpaginator)
    """

    def paginate(
        self,
        *,
        repositoryName: str,
        registryId: str = ...,
        imageIds: Sequence["ImageIdentifierTypeDef"] = ...,
        filter: "LifecyclePolicyPreviewFilterTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetLifecyclePolicyPreviewResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ecr.html#ECR.Paginator.GetLifecyclePolicyPreview.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html#getlifecyclepolicypreviewpaginator)
        """

class ListImagesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ecr.html#ECR.Paginator.ListImages)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html#listimagespaginator)
    """

    def paginate(
        self,
        *,
        repositoryName: str,
        registryId: str = ...,
        filter: "ListImagesFilterTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/ecr.html#ECR.Paginator.ListImages.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr/paginators.html#listimagespaginator)
        """
