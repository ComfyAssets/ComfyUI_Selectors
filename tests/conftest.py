"""
Pytest configuration and fixtures for ComfyUI Selectors tests.
"""

import os
import sys

import pytest

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "nodes"))

# Set up mock ComfyUI modules immediately
# Import after path setup for proper module resolution
from tests.mocks.mock_comfy import MockSamplers, MAX_RESOLUTION  # noqa: E402

# Mock comfy module
comfy_module = type("MockComfy", (), {})()
comfy_module.samplers = MockSamplers
sys.modules["comfy"] = comfy_module
sys.modules["comfy.samplers"] = MockSamplers

# Mock nodes module
nodes_module = type("MockNodes", (), {})()
nodes_module.MAX_RESOLUTION = MAX_RESOLUTION
sys.modules["nodes"] = nodes_module


@pytest.fixture(scope="session", autouse=True)
def setup_mock_comfy():
    """Set up mock ComfyUI modules for testing."""
    from tests.mocks.mock_comfy import MockSamplers, MAX_RESOLUTION

    # Mock comfy module
    comfy_module = type("MockComfy", (), {})()
    comfy_module.samplers = MockSamplers
    sys.modules["comfy"] = comfy_module
    sys.modules["comfy.samplers"] = MockSamplers

    # Mock nodes module
    nodes_module = type("MockNodes", (), {})()
    nodes_module.MAX_RESOLUTION = MAX_RESOLUTION
    sys.modules["nodes"] = nodes_module

    return True


@pytest.fixture
def sampler_selector():
    """Fixture for SamplerSelector node."""
    from sampler_selector import SamplerSelector

    return SamplerSelector()


@pytest.fixture
def scheduler_selector():
    """Fixture for SchedulerSelector node."""
    from scheduler_selector import SchedulerSelector

    return SchedulerSelector()


@pytest.fixture
def seed_generator():
    """Fixture for SeedGenerator node."""
    from seed_generator import SeedGenerator

    return SeedGenerator()


@pytest.fixture
def width_node():
    """Fixture for WidthNode node."""
    from width_node import WidthNode

    return WidthNode()


@pytest.fixture
def height_node():
    """Fixture for HeightNode node."""
    from height_node import HeightNode

    return HeightNode()


@pytest.fixture
def width_height_node():
    """Fixture for WidthHeightNode node."""
    from width_height_node import WidthHeightNode

    return WidthHeightNode()


@pytest.fixture
def all_nodes():
    """Fixture that returns all node classes for testing."""
    from height_node import HeightNode
    from sampler_selector import SamplerSelector
    from scheduler_selector import SchedulerSelector
    from seed_generator import SeedGenerator
    from width_height_node import WidthHeightNode
    from width_node import WidthNode

    return {
        "SamplerSelector": SamplerSelector,
        "SchedulerSelector": SchedulerSelector,
        "SeedGenerator": SeedGenerator,
        "WidthNode": WidthNode,
        "HeightNode": HeightNode,
        "WidthHeightNode": WidthHeightNode,
    }
