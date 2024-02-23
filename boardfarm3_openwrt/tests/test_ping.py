"""Check if ping works between lan clients."""

import pytest
from boardfarm3.lib.device_manager import DeviceManager
from boardfarm3.templates.lan import LAN
from pytest_boardfarm3.lib.test_logger import TestLogger

from boardfarm3_openwrt.use_cases.ping import ping


@pytest.mark.env_req(
    {
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": [
                    "dual",
                    "ipv4",
                ],
                "lan_clients": [{}, {}],
            },
        },
    }
)
def test_ping(bf_logger: TestLogger, device_manager: DeviceManager) -> None:
    """Check if ping works between lan clients."""
    lan1, lan2, *_ = device_manager.get_devices_by_type(
        LAN,  # type: ignore[type-abstract]
    ).values()
    bf_logger.log_step("Step1: Perform ping between lan1 and lan2")
    assert ping(
        lan1,
        lan2,
        ping_count=10,
        ping_interface=lan1.iface_dut,
        timeout=50,
        json_output=False,
    )
