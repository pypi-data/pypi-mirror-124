"""
Type annotations for iot1click-devices service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_iot1click_devices import IoT1ClickDevicesServiceClient
    from mypy_boto3_iot1click_devices.paginator import (
        ListDeviceEventsPaginator,
        ListDevicesPaginator,
    )

    client: IoT1ClickDevicesServiceClient = boto3.client("iot1click-devices")

    list_device_events_paginator: ListDeviceEventsPaginator = client.get_paginator("list_device_events")
    list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListDeviceEventsResponseTypeDef,
    ListDevicesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListDeviceEventsPaginator", "ListDevicesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDeviceEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Paginator.ListDeviceEvents)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/paginators.html#listdeviceeventspaginator)
    """

    def paginate(
        self,
        *,
        DeviceId: str,
        FromTimeStamp: Union[datetime, str],
        ToTimeStamp: Union[datetime, str],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeviceEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Paginator.ListDeviceEvents.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/paginators.html#listdeviceeventspaginator)
        """

class ListDevicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Paginator.ListDevices)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/paginators.html#listdevicespaginator)
    """

    def paginate(
        self, *, DeviceType: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.64/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Paginator.ListDevices.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iot1click_devices/paginators.html#listdevicespaginator)
        """
