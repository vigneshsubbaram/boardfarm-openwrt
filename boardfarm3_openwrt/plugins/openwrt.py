"""Boardfarm plugin for OpenWRT devices."""

from boardfarm3 import hookimpl
from boardfarm3.devices.base_devices import BoardfarmDevice

from boardfarm3_openwrt.devices.openwrt import OpenWRT


@hookimpl
def boardfarm_add_devices() -> dict[str, type[BoardfarmDevice]]:
    """Add devices to known devices for deployment.

    :return: devices dictionary
    :rtype: dict[str, type[BoardfarmDevice]]
    """
    return {
        "OpenWRT": OpenWRT,
    }
