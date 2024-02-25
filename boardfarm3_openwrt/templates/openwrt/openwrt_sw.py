"""OpenWRT SW Template."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipaddress import IPv4Address, IPv4Network, IPv6Address

    from boardfarm3.lib.boardfarm_pexpect import BoardfarmPexpect
    from boardfarm3.lib.networking import DNS, IptablesFirewall


class OpenWRTSW(ABC):
    """OpenWRT Software Template."""

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
    def lan_gateway_ipv4(self) -> IPv4Address:
        """LAN Gateway IPv4 address."""
        raise NotImplementedError

    @property
    @abstractmethod
    def lan_gateway_ipv6(self) -> IPv6Address:
        """LAN Gateway IPv6 address."""
        raise NotImplementedError

    @property
    @abstractmethod
    def lan_network_ipv4(self) -> IPv4Network:
        """LAN IPv4 network."""
        raise NotImplementedError

    @property
    @abstractmethod
    def dns(self) -> DNS:
        """DNS component of OpenWRT software."""
        raise NotImplementedError

    @property
    @abstractmethod
    def firewall(self) -> IptablesFirewall:
        """Firewall component of OpenWRT software."""
        raise NotImplementedError

    @abstractmethod
    def get_interface_ipv4addr(self, interface: str) -> str:
        """Return given interface IPv4 address.

        :param interface: interface name
        :return: IPv4 address
        """
        raise NotImplementedError

    @abstractmethod
    def get_interface_ipv6addr(self, interface: str) -> str:
        """Return given interface IPv6 address.

        :param interface: interface name
        :return: IPv6 address
        """
        raise NotImplementedError

    @abstractmethod
    def get_interface_mac_addr(self, interface: str) -> str:
        """Return given interface mac address.

        :param interface: interface name
        :return: mac address of the given interface
        """
        raise NotImplementedError

    @abstractmethod
    def _get_console(self, usage: str) -> BoardfarmPexpect:
        """Return console instance for the given usage.

        :param usage: usage of the console(dmcli/networking/wifi)
        :type usage: str
        :return: console instance for the given usage
        :rtype: BoardfarmPexpect
        """
        raise NotImplementedError
