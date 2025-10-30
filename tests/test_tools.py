import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import MagicMock
from tools.mcp_client import MCPClient
from tools.metrics_tool import MetricsTracker

@pytest.fixture
def mcp():
    client = MCPClient()
    # Mock the query method
    client.query = MagicMock(return_value={"response": "mock"})
    return client

@pytest.fixture
def metrics():
    return MetricsTracker()

def test_mcp_client_call(mcp):
    result = mcp.query({"test": "data"})
    assert isinstance(result, dict)
    assert result.get("response") == "mock"

def test_metrics_tracker(metrics):
    try:
        metrics.log_event("test_event", {"key": "value"})
    except Exception as e:
        pytest.fail(f"MetricsTracker failed: {e}")

