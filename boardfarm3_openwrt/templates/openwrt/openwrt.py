"""OpenWRT device template."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipaddress import IPv4Address, IPv4Network

    from boardfarm3_openwrt.templates.openwrt.openwrt_hw import OpenWRTHW
    from boardfarm3_openwrt.templates.openwrt.openwrt_sw import OpenWRTSW


# pylint: disable=too-many-public-methods,too-many-instance-attributes


class OpenWRT(ABC):
    """OpenWRT device Template."""

    @property
    @abstractmethod
    def hw(self) -> OpenWRTHW:  # pylint: disable=invalid-name
        """OpenWRT hardware."""
        raise NotImplementedError

    @property
    @abstractmethod
    def sw(self) -> OpenWRTSW:  # pylint: disable=invalid-name
        """OpenWRT Software."""
        raise NotImplementedError

    @property
    @abstractmethod
    def mac(self) -> str:
        """MAC Address."""
        raise NotImplementedError

    @property
    @abstractmethod
    def wan_iface(self) -> str:
        """WAN interface name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def lan_iface(self) -> str:
        """LAN interface name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def gui_password(self) -> str:
        """GUI login password."""
        raise NotImplementedError

    @property
    @abstractmethod
    def lan_gateway(self) -> IPv4Address:
        """LAN Gateway IPv4 address."""
        raise NotImplementedError

    @property
    @abstractmethod
    def lan_network(self) -> IPv4Network:
        """LAN IPv4 network."""
        raise NotImplementedError

    @abstractmethod
    def get_interface_ipaddr(self, interface: str) -> str:
        """Return given interface IPv4 address.

        :param interface: interface name
        :type interface: str
        :return: IPv4 address
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def get_interface_ip6addr(self, interface: str) -> str:
        """Return given interface IPv6 address.

        :param interface: interface name
        :type interface: str
        :return: IPv6 address
        :rtype: str
        """
        raise NotImplementedError
