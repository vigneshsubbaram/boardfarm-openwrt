"""Sample ping use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from boardfarm3.templates.lan import LAN
    from boardfarm3.templates.wan import WAN


def ping(  # noqa: PLR0913
    src: LAN | WAN,
    dst: LAN | WAN,
    ping_count: int = 4,
    ping_interface: str | None = None,
    timeout: int = 50,
    json_output: bool = False,
) -> bool | dict[str, Any]:
    """Use case to demostrate ping from lan to wan or vice-versa.

    :param src: Source device
    :type src: LAN | WAN
    :param dst: Destination device
    :type dst: LAN | WAN
    :param ping_count: number of concurrent pings, defaults to 4
    :type ping_count: int, optional
    :param ping_interface: ping via interface, defaults to None
    :type ping_interface: str | None, optional
    :param timeout: timeout, defaults to 50
    :type timeout: int, optional
    :param json_output: True if ping output in dictionary format else False,
        defaults to False, defaults to False
    :type json_output: bool, optional
    :return: bool or dict of ping output
    :rtype: bool | dict[str, Any]
    """
    return src.ping(
        dst.get_eth_interface_ipv4_address(),
        ping_count,
        ping_interface,
        timeout=timeout,
        json_output=json_output,
    )
