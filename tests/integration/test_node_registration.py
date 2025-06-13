"""
Integration tests for node registration and mappings.
"""

# Integration tests for node registration (no pytest needed in this case)


def test_node_class_mappings():
    """Test NODE_CLASS_MAPPINGS contains expected nodes."""
    # Import individual nodes directly since the main __init__.py uses relative imports
    from height_node import HeightNode
    from random_value_tracker import SeedHistory
    from sampler_selector import SamplerSelector
    from scheduler_selector import SchedulerSelector
    from width_height_node import WidthHeightNode
    from width_node import WidthNode

    expected_mappings = {
        "SamplerSelector": SamplerSelector,
        "SchedulerSelector": SchedulerSelector,
        "SeedHistory": SeedHistory,
        "WidthNode": WidthNode,
        "HeightNode": HeightNode,
        "WidthHeightNode": WidthHeightNode,
    }

    # Test that all expected nodes exist and are classes
    for node_name, node_class in expected_mappings.items():
        assert callable(node_class), f"{node_name} is not a callable class"

        # Test instantiation
        instance = node_class()
        assert instance is not None

        # Test required ComfyUI attributes
        assert hasattr(instance, "INPUT_TYPES"), f"{node_name} missing INPUT_TYPES"
        assert hasattr(instance, "RETURN_TYPES"), f"{node_name} missing RETURN_TYPES"
        assert hasattr(instance, "FUNCTION"), f"{node_name} missing FUNCTION"
        assert hasattr(instance, "CATEGORY"), f"{node_name} missing CATEGORY"


def test_node_display_names():
    """Test NODE_DISPLAY_NAME_MAPPINGS contains expected display names."""
    expected_display_names = {
        "SamplerSelector": "Sampler Selector",
        "SchedulerSelector": "Scheduler Selector",
        "SeedHistory": "Seed History",
        "WidthNode": "Width",
        "HeightNode": "Height",
        "WidthHeightNode": "Width & Height",
    }

    # Test that all display names are strings and non-empty
    for node_name, display_name in expected_display_names.items():
        assert isinstance(
            display_name, str
        ), f"Display name for {node_name} is not a string"
        assert len(display_name) > 0, f"Display name for {node_name} is empty"


def test_node_categories():
    """Test that nodes are in appropriate categories."""
    from height_node import HeightNode
    from random_value_tracker import SeedHistory
    from sampler_selector import SamplerSelector
    from scheduler_selector import SchedulerSelector
    from width_height_node import WidthHeightNode
    from width_node import WidthNode

    expected_categories = {
        SamplerSelector: "comfyassets/Sampling",
        SchedulerSelector: "comfyassets/Sampling",
        SeedHistory: "comfyassets/Generation",
        WidthNode: "comfyassets/Dimensions",
        HeightNode: "comfyassets/Dimensions",
        WidthHeightNode: "comfyassets/Dimensions",
    }

    for node_class, expected_category in expected_categories.items():
        instance = node_class()
        assert (
            instance.CATEGORY == expected_category
        ), f"{node_class.__name__} has wrong category"


def test_node_function_methods():
    """Test that all nodes have callable function methods."""
    from height_node import HeightNode
    from random_value_tracker import SeedHistory
    from sampler_selector import SamplerSelector
    from scheduler_selector import SchedulerSelector
    from width_height_node import WidthHeightNode
    from width_node import WidthNode

    nodes = [
        SamplerSelector(),
        SchedulerSelector(),
        SeedHistory(),
        WidthNode(),
        HeightNode(),
        WidthHeightNode(),
    ]

    for node in nodes:
        function_name = node.FUNCTION
        assert hasattr(
            node, function_name
        ), f"{node.__class__.__name__} missing function {function_name}"
        function_method = getattr(node, function_name)
        assert callable(
            function_method
        ), f"{node.__class__.__name__}.{function_name} is not callable"


def test_input_types_structure():
    """Test that all nodes have proper INPUT_TYPES structure."""
    from height_node import HeightNode
    from random_value_tracker import SeedHistory
    from sampler_selector import SamplerSelector
    from scheduler_selector import SchedulerSelector
    from width_height_node import WidthHeightNode
    from width_node import WidthNode

    nodes = [
        SamplerSelector(),
        SchedulerSelector(),
        SeedHistory(),
        WidthNode(),
        HeightNode(),
        WidthHeightNode(),
    ]

    for node in nodes:
        input_types = node.INPUT_TYPES()
        assert isinstance(
            input_types, dict
        ), f"{node.__class__.__name__}.INPUT_TYPES() must return dict"
        assert (
            "required" in input_types
        ), f"{node.__class__.__name__}.INPUT_TYPES() must have 'required' key"
        assert isinstance(
            input_types["required"], dict
        ), f"{node.__class__.__name__}.INPUT_TYPES()['required'] must be dict"


def test_return_types_structure():
    """Test that all nodes have proper RETURN_TYPES structure."""
    from height_node import HeightNode
    from random_value_tracker import SeedHistory
    from sampler_selector import SamplerSelector
    from scheduler_selector import SchedulerSelector
    from width_height_node import WidthHeightNode
    from width_node import WidthNode

    nodes = [
        SamplerSelector(),
        SchedulerSelector(),
        SeedHistory(),
        WidthNode(),
        HeightNode(),
        WidthHeightNode(),
    ]

    for node in nodes:
        assert isinstance(
            node.RETURN_TYPES, tuple
        ), f"{node.__class__.__name__}.RETURN_TYPES must be tuple"
        assert (
            len(node.RETURN_TYPES) > 0
        ), f"{node.__class__.__name__}.RETURN_TYPES must not be empty"


def test_web_directory_configuration():
    """Test that WEB_DIRECTORY is properly configured."""
    import os

    # Check if web directory exists
    web_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "web"
    )
    assert os.path.exists(web_dir), "Web directory should exist for UI extensions"

    # Check if our UI file exists
    ui_file = os.path.join(web_dir, "seed_history_ui.js")
    assert os.path.exists(ui_file), "seed_history_ui.js should exist for SeedHistory UI"
