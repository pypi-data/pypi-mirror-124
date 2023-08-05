"""
Type annotations for applicationcostprofiler service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_applicationcostprofiler/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_applicationcostprofiler import ApplicationCostProfilerClient
    from mypy_boto3_applicationcostprofiler.paginator import (
        ListReportDefinitionsPaginator,
    )

    client: ApplicationCostProfilerClient = boto3.client("applicationcostprofiler")

    list_report_definitions_paginator: ListReportDefinitionsPaginator = client.get_paginator("list_report_definitions")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListReportDefinitionsResultTypeDef, PaginatorConfigTypeDef

__all__ = ("ListReportDefinitionsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListReportDefinitionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/applicationcostprofiler.html#ApplicationCostProfiler.Paginator.ListReportDefinitions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_applicationcostprofiler/paginators.html#listreportdefinitionspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListReportDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/applicationcostprofiler.html#ApplicationCostProfiler.Paginator.ListReportDefinitions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_applicationcostprofiler/paginators.html#listreportdefinitionspaginator)
        """
