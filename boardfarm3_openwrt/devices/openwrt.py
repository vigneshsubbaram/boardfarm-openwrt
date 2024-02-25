"""OpenWRT device module."""

import logging
from argparse import Namespace
from ipaddress import IPv4Address, IPv4Network

from boardfarm3 import hookimpl
from boardfarm3.devices.base_devices.boardfarm_device import BoardfarmDevice
from boardfarm3.lib.boardfarm_pexpect import BoardfarmPexpect

from boardfarm3_openwrt.lib.openwrt_hw import OpenWRTHW
from boardfarm3_openwrt.lib.openwrt_sw import OpenWRTSW
from boardfarm3_openwrt.templates.openwrt.openwrt import OpenWRT as OpenWRTTemplate

_LOGGER = logging.getLogger(__name__)


class OpenWRT(BoardfarmDevice, OpenWRTTemplate):
    """OpenWRT device."""

    def __init__(self, config: dict, cmdline_args: Namespace) -> None:
        """Initialize OpenWRT device.

        :param config: device configuration
        :param cmdline_args: command line arguments
        """
        self._hw = OpenWRTHW(config, cmdline_args)
        self._sw: OpenWRTSW = None
        self._config = config

    @hookimpl(tryfirst=True)
    def boardfarm_skip_boot(self) -> None:
        """Boardfarm skip boot hook implementation."""
        _LOGGER.info(
            "Initializing %s(%s) device with skip-boot option",
            self.device_name,
            self.device_type,
        )
        self._hw.connect_to_console(self.device_name)
        self._sw = OpenWRTSW(self._hw)

    @hookimpl(tryfirst=True)
    async def boardfarm_skip_boot_async(self) -> None:
        """Boardfarm async skip boot hook implementation."""
        _LOGGER.info(
            "Initializing %s(%s) device with async skip-boot option",
            self.device_name,
            self.device_type,
        )
        await self._hw.connect_to_console_async(self.device_name)
        self._sw = OpenWRTSW(self._hw)

    @property
    def hw(self) -> OpenWRTHW:  # pylint: disable=invalid-name
        """Openwrt hardware.

        :return: OpenWRT hardware.
        :rtype: OpenWRTHW
        """
        return self._hw

    @property
    def sw(self) -> OpenWRTSW:  # pylint: disable=invalid-name
        """Openwrt Software.

        :return: OpenWRT Software.
        :rtype: OpenWRTSW
        """
        return self._sw

    @property
    def mac(self) -> str:
        """MAC Address.

        :return: MAC Address.
        :rtype: str
        """
        return self._config.get("mac")

    @property
    def wan_iface(self) -> str:
        """WAN interface name.

        :return: WAN interface name.
        :rtype: str
        """
        return "br-wan"

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
    def lan_gateway(self) -> IPv4Address:
        """LAN Gateway IPv4 address.

        :return: LAN Gateway IPv4 address.
        :rtype: IPv4Address
        """
        return IPv4Address("192.168.0.1")

    @property
    def lan_network(self) -> IPv4Network:
        """LAN IPv4 network.

        :return: LAN IPv4 network.
        :rtype: IPv4Network
        """
        return IPv4Network("192.168.0.0/24")

    def get_interface_ipaddr(self, interface: str) -> str:
        """Return given interface IPv4 address.

        :param interface: interface name
        :return: IPv4 address
        """
        return self.sw.get_interface_ipv4addr(interface)

    def get_interface_ip6addr(self, interface: str) -> str:
        """Return given interface IPv6 address.

        :param interface: interface name
        :return: IPv6 address
        """
        return self.sw.get_interface_ipv6addr(interface)

    def get_interactive_consoles(self) -> dict[str, BoardfarmPexpect]:
        """Get interactive consoles of the device.

        :return: device interactive consoles
        :rtype: dict[str, BoardfarmPexpect]
        """
        return self.hw.get_interactive_consoles()
