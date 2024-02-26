"""OpenWRT hardware implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from boardfarm3.lib.connection_factory import connection_factory

from boardfarm3_openwrt.templates.openwrt.openwrt_hw import (
    OpenWRTHW as OpenWRTHWTemplate,
)

if TYPE_CHECKING:
    from argparse import Namespace

    from boardfarm3.lib.boardfarm_pexpect import BoardfarmPexpect


class OpenWRTHW(OpenWRTHWTemplate):
    """OpenWRT hardware implementation."""

    def __init__(self, config: dict[str, Any], cmdline_args: Namespace) -> None:
        """Initialize OpenWRT hardware.

        :param config: OpenWRT config
        :type config: dict[str, Any]
        :param cmdline_args: command line arguments
        :type cmdline_args: Namespace
        """
        self._config = config
        self._cmdline_args = cmdline_args
        self._console: BoardfarmPexpect | None = None
        self._shell_prompt: list[str] = [r"root@OpenWrt:~#"]

    @property
    def config(self) -> dict[str, Any]:
        """Device config.

        :return: Device config.
        :rtype: dict[str, Any]
        """
        return self._config

    def _connect_to_serial_console(self, device_name: str) -> BoardfarmPexpect:
        """Establish connection to serial console.

        :param device_name: device name
        :type device_name: str
        :return: serial console instance
        :rtype: BoardfarmPexpect
        """
        return connection_factory(
            self._config.get("connection_type"),
            f"{device_name}.console",
            username=self._username,
            password=self._password,
            ip_addr=self._ipaddr,
            port=self._port,
            shell_prompt=self._shell_prompt,
            save_console_logs=self._cmdline_args.save_console_logs,
        )

    @property
    def _ipaddr(self) -> str:
        """Management IP address of the device.

        :return: ipaddress of the device
        :rtype: str
        """
        return self._config.get("ipaddr")

    @property
    def _port(self) -> str:
        """Management connection port of the device.

        :return: management connection port of the device
        :rtype: str
        """
        return self._config.get("port", "22")

    @property
    def _username(self) -> str:
        """Management connection username.

        :return: management iface username
        :rtype: str
        """
        return self._config.get("username", "root")

    @property
    def _password(self) -> str:
        """Management connection password.

        :return: management iface password
        :rtype: str
        """
        return self._config.get("password", "root")

    def connect_to_console(self, device_name: str) -> None:
        """Establish connection to the OpenWRT console.

        :param device_name: device to be connected
        :type device_name: str
        """
        self._console = self._connect_to_serial_console(device_name)
        self._console.login_to_server(self._password)

    async def connect_to_console_async(self, device_name: str) -> None:
        """Establish connection to the OpenWRT console.

        :param device_name: device to be connected
        :type device_name: str
        """
        self._console = self._connect_to_serial_console(device_name)
        await self._console.login_to_server_async(self._password)

    def disconnect_from_console(self) -> None:
        """Disconnect/Close the console connections."""
        if self._console is not None:
            self._console.close()

    @property
    def mac_address(self) -> str:
        """Get CPE MAC address.

        :return: CPE MAC address.
        :rtype: str
        """
        return self._config.get("mac")

    def get_interactive_consoles(self) -> dict[str, BoardfarmPexpect]:
        """Get interactive consoles of the device.

        :return: device interactive consoles
        :rtype: dict[str, BoardfarmPexpect]
        """
        return {"console": self._console}

    def get_console(self) -> BoardfarmPexpect:
        """Return console instance.

        :return: console instance
        :rtype: BoardfarmPexpect
        """
        return self._console
