"""
Integration tests for the main module and node registration.
"""

import pytest  # noqa: F401


def test_main_module_import():
    """Test that the main module can be imported successfully."""
    import os
    import sys

    # Import the main module properly
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "main_init",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "__init__.py"
        ),
    )
    main_init = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_init)

    assert hasattr(main_init, "NODE_CLASS_MAPPINGS")
    assert hasattr(main_init, "NODE_DISPLAY_NAME_MAPPINGS")


def test_node_mappings_consistency():
    """Test that node mappings are consistent."""
    import importlib.util
    import os
    import sys

    # Import the main module properly
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    spec = importlib.util.spec_from_file_location(
        "main_init",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "__init__.py"
        ),
    )
    main_init = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_init)

    node_classes = main_init.NODE_CLASS_MAPPINGS
    display_names = main_init.NODE_DISPLAY_NAME_MAPPINGS

    # Check that mappings have the same keys
    assert set(node_classes.keys()) == set(display_names.keys())

    # Check that all expected nodes are registered
    expected_nodes = {
        "SamplerSelector",
        "SchedulerSelector",
        "SeedGenerator",
        "WidthNode",
        "HeightNode",
        "WidthHeightNode",
    }
    assert set(node_classes.keys()) == expected_nodes


def test_registered_nodes_are_classes():
    """Test that registered nodes are actual classes."""
    import importlib.util
    import os
    import sys

    # Import the main module properly
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    spec = importlib.util.spec_from_file_location(
        "main_init",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "__init__.py"
        ),
    )
    main_init = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_init)

    for node_name, node_class in main_init.NODE_CLASS_MAPPINGS.items():
        assert callable(node_class), f"{node_name} is not a callable class"

        # Test instantiation
        instance = node_class()
        assert instance is not None


def test_display_names_are_strings():
    """Test that display names are strings."""
    import importlib.util
    import os
    import sys

    # Import the main module properly
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    spec = importlib.util.spec_from_file_location(
        "main_init",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "__init__.py"
        ),
    )
    main_init = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_init)

    for node_name, display_name in main_init.NODE_DISPLAY_NAME_MAPPINGS.items():
        assert isinstance(
            display_name, str
        ), f"Display name for {node_name} is not a string"
        assert len(display_name) > 0, f"Display name for {node_name} is empty"
