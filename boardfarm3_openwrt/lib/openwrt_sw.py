"""OpenWRT software module."""

import re
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Interface

from boardfarm3.lib.boardfarm_pexpect import BoardfarmPexpect
from boardfarm3.lib.networking import DNS, IptablesFirewall

from boardfarm3_openwrt.lib.openwrt_hw import OpenWRTHW
from boardfarm3_openwrt.templates.openwrt.openwrt_sw import (
    OpenWRTSW as OpenWRTSWTemplate,
)


class OpenWRTSW(OpenWRTSWTemplate):
    """OpenWRT software."""

    def __init__(self, hardware: OpenWRTHW) -> None:
        """Initialise the OpenWRT software.

        :param hardware: OpenWRT hardware instance
        :type hardware: OpenWRTHW
        """
        self._hw = hardware
        self._console = hardware.get_console()
        self._firewall = IptablesFirewall(self._get_console("networking"))
        self._dns = DNS(self._get_console("networking"), hardware.config.get("name"))

    @property
    def lan_iface(self) -> str:
        """LAN interface name.

        :return: LAN interface name.
        :rtype: str
        """
        return "br-lan"

    @property
    def gui_password(self) -> str:
        """GUI login password.

        :return: GUI login password.
        :rtype: str
        """
        return "admin"

    @property
    def lan_gateway_ipv4(self) -> IPv4Address:
        """LAN Gateway IPv4 address.

        :return: LAN Gateway IPv4 address.
        :rtype: IPv4Address
        """
        return IPv4Address(self.get_interface_ipv4addr(self.lan_iface))

    @property
    def lan_gateway_ipv6(self) -> IPv6Address:
        """LAN Gateway IPv6 address.

        :return: LAN Gateway IPv6 address.
        :rtype: IPv6Address
        """
        return IPv6Address(self.get_interface_ipv6addr(self.lan_iface))

    def get_interface_ipv4_netmask(self, interface: str) -> IPv4Address:
        """Return given interface IPv4 netmask.

        :param interface: name of the interface
        :type interface: str
        :return: netmask of the interface
        :rtype: IPv4Address
        """
        output = self._get_console("networking").execute_command(
            f"ifconfig {interface}",
        )
        netmask = output.split("Mask:")[-1].split()[0]
        return IPv4Address(netmask)

    @property
    def lan_network_ipv4(self) -> IPv4Network:
        """LAN IPv4 network.

        :return: LAN IPv4 network.
        :rtype: IPv4Network
        """
        lan_network_mask = self.get_interface_ipv4_netmask(self.lan_iface)
        return IPv4Network(f"{self.lan_gateway_ipv4}/{lan_network_mask}", strict=False)

    def _get_console(self, usage: str) -> BoardfarmPexpect:
        """Return console instance for the given usage.

        :param usage: usage of the console(default_shell/networking/wifi)
        :type usage: str
        :raises ValueError: if unknown console
        :return: console instance for the given usage
        :rtype: BoardfarmPexpect
        """
        if usage in ("networking", "wifi", "default_shell"):
            return self._console
        err_msg = f"Unknown console usage: {usage}"
        raise ValueError(err_msg)

    @property
    def dns(self) -> DNS:
        """DNS component of OpenWRT software.

        :return: DNS component of OpenWRT software.
        :rtype: DNS
        """
        return self._dns

    @property
    def firewall(self) -> IptablesFirewall:
        """Firewall component of cpe software.

        :return: Firewall component of cpe software.
        :rtype: IptablesFirewall
        """
        return self._firewall

    def _get_nw_interface_ip_address(
        self,
        interface_name: str,
        is_ipv6: bool,
    ) -> list[str]:
        """Return network interface ip address.

        :param interface_name: interface name
        :param is_ipv6: is ipv6 address
        :returns: IP address list
        """
        prefix = "inet6" if is_ipv6 else "inet"
        ip_regex = prefix + r"\s(?:addr:)?\s*([^\s/]+)"
        output = self._get_console("networking").execute_command(
            f"ifconfig {interface_name}",
        )
        return re.findall(ip_regex, output)

    def get_interface_ipv4addr(self, interface: str) -> str:
        """Return given interface IPv4 address.

        :param interface: interface name
        :type interface: str
        :raises ValueError: If failed to get the IPv4 address of the interface
        :return: IPv4 address
        :rtype: str
        """
        if ips := self._get_nw_interface_ip_address(interface, is_ipv6=False):
            return ips[0]
        err_msg = f"Failed to get IPv4 address of {interface} interface"
        raise ValueError(err_msg)

    def _get_interface_ipv6_address(self, interface: str, address_type: str) -> str:
        """Return IPv6 address of the given network interface.

        :param interface: network interface name
        :type interface: str
        :param address_type: ipv6 address type
        :type address_type: str
        :raises ValueError: If failed to get the IPv6 address of the interface
        :return: IPv6 address of the given interface
        :rtype: str
        """
        address_type = address_type.replace("-", "_")
        ip_addresses = self._get_nw_interface_ip_address(interface, is_ipv6=True)
        for ip_addr in ip_addresses:
            if getattr(IPv6Interface(ip_addr), f"is_{address_type}"):
                return ip_addr
        err_msg = f"Failed to get IPv6 address of {interface} {address_type} address"
        raise ValueError(err_msg)

    def get_interface_ipv6addr(self, interface: str) -> str:
        """Return given interface IPv6 address.

        :param interface: interface name
        :return: IPv6 address
        """
        return self._get_interface_ipv6_address(interface, "global")

    def get_interface_mac_addr(self, interface: str) -> str:
        """Return given interface mac address.

        :param interface: interface name
        :return: mac address of the given interface
        """
        return (
            self._get_console("networking")
            .execute_command(f"cat /sys/class/net/{interface}/address")
            .strip()
        )
