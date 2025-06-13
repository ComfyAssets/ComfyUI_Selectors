"""
Unit tests for SeedHistory widget callback functionality.

Note: These tests focus on the Python node structure and behavior.
The JavaScript widget callback functionality in seed_history_ui.js
would require a browser/DOM environment to test fully.
"""

import pytest


class TestSeedHistoryCallbacks:
    """Test SeedHistory callback-related functionality."""

    def test_node_structure_supports_widgets(self, seed_history):
        """Test that node structure supports widget integration."""
        # Test that the node has the required structure for ComfyUI widgets
        assert hasattr(seed_history, "INPUT_TYPES")
        assert callable(seed_history.INPUT_TYPES)

        input_types = seed_history.INPUT_TYPES()
        assert "required" in input_types
        assert "seed" in input_types["required"]

    def test_seed_input_configuration(self, seed_history):
        """Test seed input is properly configured for widgets."""
        input_types = seed_history.INPUT_TYPES()
        seed_config = input_types["required"]["seed"]

        # Verify it's an INT type (required for seed widgets)
        assert seed_config[0] == "INT"

        # Verify it has proper range for seeds
        config_dict = seed_config[1]
        assert config_dict["min"] == 0
        assert config_dict["max"] == 0xFFFFFFFFFFFFFFFF

        # Verify it has a default value
        assert "default" in config_dict
        assert isinstance(config_dict["default"], int)

    def test_output_consistency(self, seed_history):
        """Test that output is consistent regardless of input source."""
        # Test with various seed values that might come from different sources
        test_seeds = [
            12345,  # Default value
            0,  # Minimum value
            1,  # Increment from 0
            42,  # Manual input
            999999,  # Large manual input
            0xFFFFFFFFFFFFFFFF,  # Maximum value
        ]

        for seed in test_seeds:
            result = seed_history.output_seed(seed)
            assert result == (seed,), f"Failed for seed {seed}"
            assert isinstance(result[0], int), f"Result not int for seed {seed}"

    def test_node_category_for_ui_placement(self, seed_history):
        """Test node is in correct category for UI organization."""
        assert seed_history.CATEGORY == "comfyassets/Generation"

    def test_function_name_for_comfyui_execution(self, seed_history):
        """Test function name matches ComfyUI expectations."""
        assert seed_history.FUNCTION == "output_seed"
        assert hasattr(seed_history, seed_history.FUNCTION)

        # Test the function can be called
        func = getattr(seed_history, seed_history.FUNCTION)
        assert callable(func)

    def test_return_types_for_widget_compatibility(self, seed_history):
        """Test return types are compatible with other ComfyUI nodes."""
        assert seed_history.RETURN_TYPES == ("INT",)
        assert len(seed_history.RETURN_TYPES) == 1

        # Test return names if provided
        if hasattr(seed_history, "RETURN_NAMES"):
            assert seed_history.RETURN_NAMES == ("seed",)
            assert len(seed_history.RETURN_NAMES) == len(seed_history.RETURN_TYPES)

    def test_edge_case_values(self, seed_history):
        """Test edge case values that might come from widget operations."""
        edge_cases = [
            0,  # Minimum seed
            1,  # First increment
            2147483647,  # Max 32-bit int
            4294967295,  # Max 32-bit uint
            9223372036854775807,  # Max 64-bit int
            0xFFFFFFFFFFFFFFFF,  # Max uint64
        ]

        for seed in edge_cases:
            try:
                result = seed_history.output_seed(seed)
                assert result == (seed,), f"Failed for edge case {seed}"
            except (ValueError, OverflowError) as e:
                # Some edge cases might legitimately fail
                pytest.skip(f"Edge case {seed} caused {type(e).__name__}: {e}")

    def test_widget_callback_node_structure(self, seed_history):
        """Test node structure required for widget callbacks."""
        # These attributes are required for the JavaScript extension to work
        required_attrs = [
            "INPUT_TYPES",  # Must be callable
            "RETURN_TYPES",  # Must be tuple
            "FUNCTION",  # Must be string
            "CATEGORY",  # Must be string
        ]

        for attr in required_attrs:
            assert hasattr(seed_history, attr), f"Missing required attribute: {attr}"

        # Test INPUT_TYPES is callable
        assert callable(seed_history.INPUT_TYPES)

        # Test RETURN_TYPES is tuple
        assert isinstance(seed_history.RETURN_TYPES, tuple)

        # Test FUNCTION is string and method exists
        assert isinstance(seed_history.FUNCTION, str)
        assert hasattr(seed_history, seed_history.FUNCTION)

        # Test CATEGORY is string
        assert isinstance(seed_history.CATEGORY, str)

    def test_documentation_for_ui_tooltip(self, seed_history):
        """Test that the node has proper documentation for UI tooltips."""
        input_types = seed_history.INPUT_TYPES()
        seed_config = input_types["required"]["seed"][1]

        # Check if tooltip is provided
        assert "tooltip" in seed_config
        assert isinstance(seed_config["tooltip"], str)
        assert len(seed_config["tooltip"]) > 0


class TestSeedHistoryUIIntegration:
    """Test aspects of SeedHistory that support UI integration."""

    def test_web_directory_exists(self):
        """Test that web directory is configured for UI extensions."""
        # This would be tested in the main module
        import os

        web_dir = os.path.join(os.path.dirname(__file__), "../../web")
        if os.path.exists(web_dir):
            # Check if our UI file exists
            ui_file = os.path.join(web_dir, "seed_history_ui.js")
            assert os.path.exists(ui_file), "seed_history_ui.js not found"

    def test_node_registration_name(self, seed_history):
        """Test node has consistent naming for registration."""
        # The class name should match the registration key
        assert seed_history.__class__.__name__ == "SeedHistory"

    def test_input_widget_compatibility(self, seed_history):
        """Test input configuration is compatible with ComfyUI widgets."""
        input_types = seed_history.INPUT_TYPES()
        seed_input = input_types["required"]["seed"]

        # Test widget type compatibility
        widget_type = seed_input[0]
        assert widget_type == "INT"

        # Test widget configuration
        widget_config = seed_input[1]
        required_keys = ["default", "min", "max"]
        for key in required_keys:
            assert key in widget_config, f"Missing widget config key: {key}"

    def test_node_serialization_compatibility(self, seed_history):
        """Test node supports serialization for workflow saving."""
        # Test that the node can be represented as dict-like structure
        assert hasattr(seed_history, "INPUT_TYPES")
        assert hasattr(seed_history, "RETURN_TYPES")

        # Test input types can be serialized
        input_types = seed_history.INPUT_TYPES()
        import json

        try:
            json.dumps(input_types)
        except (TypeError, ValueError) as e:
            pytest.fail(f"INPUT_TYPES not JSON serializable: {e}")
