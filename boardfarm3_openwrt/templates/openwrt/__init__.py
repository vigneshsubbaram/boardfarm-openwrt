"""Boardfarm OpenWRT CPE templates."""

from boardfarm3_openwrt.templates.openwrt.openwrt import OpenWRT
from boardfarm3_openwrt.templates.openwrt.openwrt_hw import OpenWRTHW
from boardfarm3_openwrt.templates.openwrt.openwrt_sw import OpenWRTSW

__all__ = ["OpenWRT", "OpenWRTHW", "OpenWRTSW"]
