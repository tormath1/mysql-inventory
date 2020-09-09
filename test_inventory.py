import json
from unittest.mock import (
    patch,
    MagicMock
)
import pytest

from inventory import Inventory

@pytest.fixture
@patch("mysql.connector")
def inventory(connector):
    conn = MagicMock()
    connector.connect.return_value = conn
    return Inventory(
        username="username",
        password="password",
        host="127.0.0.1",
        port=3306,
        ssl_skip_verify="True",
        database="database",
    )

def test_empty_inventory(inventory):
    res = inventory.generate()
    assert json.dumps(
        {
            "_meta": {"hostvars": {}},
        }, indent=2) == res

def test_inventory(inventory):
    cur = MagicMock()
    fetchall = MagicMock()

    fetchall.return_value = [
        {
            "hostname": "host1234",
            "baseuri": "10.10.10.10",
            "appName": "my-app",
            "buildStatus": "build_os_ok",
        },
        {
            "hostname": "host4567",
            "baseuri": "10.10.10.10",
            "appName": "my-app",
            "buildStatus": "config_ok",
        },
    ]
    cur.__enter__.return_value.fetchall = fetchall
    inventory.conn.cursor.return_value = cur

    res = inventory.generate()

    cur.__enter__().fetchall.assert_called_once()
    cur.__enter__().execute.assert_called_once_with("""SELECT \
* FROM server_physique;""")
    assert json.dumps(
        {
            "_meta": {"hostvars": {
                "host1234": {
                    "baseuri": "10.10.10.10",
                    "appName": "my-app",
                    "buildStatus": "build_os_ok",
                    "ansible_host": "10.10.10.10",
                },
                "host4567": {
                    "baseuri": "10.10.10.10",
                    "appName": "my-app",
                    "buildStatus": "config_ok",
                    "ansible_host": "10.10.10.10",
                },
            }},
            "build_os_ok": {"hosts": ["host1234"]},
            "my-app": {"hosts": ["host1234", "host4567"]},
            "config_ok": {"hosts": ["host4567"]},
        }, indent=2) == res
