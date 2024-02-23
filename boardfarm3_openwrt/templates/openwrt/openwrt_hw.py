"""OpenWRT HW Template."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from boardfarm3.lib.boardfarm_pexpect import BoardfarmPexpect


class OpenWRTHW(ABC):
    """OpenWRT hardware template."""

    @property
    def config(self) -> dict[str, Any]:
        """Device config."""
        return self._config

    @property
    @abstractmethod
    def mac_address(self) -> str:
        """Get the MAC address."""
        raise NotImplementedError

    @abstractmethod
    def connect_to_console(self, device_name: str) -> None:
        """Connect to the consoles.

        :param device_name: name of the device
        :type device_name: str
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect_from_console(self) -> None:
        """Disconnect/Close the console connections."""
        raise NotImplementedError

    @abstractmethod
    def get_interactive_consoles(self) -> dict[str, BoardfarmPexpect]:
        """Get interactive consoles of the device.

        :returns: device interactive consoles
        :rtype: Dict[str, BoardfarmPexpect]
        """
        raise NotImplementedError
