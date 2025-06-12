"""
Unit tests for ComfyUI Selector nodes.
"""

import pytest  # noqa: F401


class TestNodeStructure:
    """Test that all nodes have the required ComfyUI structure."""

    def test_node_has_required_attributes(self, all_nodes):
        """Test that each node has all required ComfyUI attributes."""
        required_attrs = ["INPUT_TYPES", "RETURN_TYPES", "FUNCTION", "CATEGORY"]

        for node_name, node_class in all_nodes.items():
            for attr in required_attrs:
                assert hasattr(
                    node_class, attr
                ), f"{node_name} missing required attribute: {attr}"

    def test_input_types_method(self, all_nodes):
        """Test that INPUT_TYPES() method returns valid structure."""
        for node_name, node_class in all_nodes.items():
            input_types = node_class.INPUT_TYPES()
            assert isinstance(
                input_types, dict
            ), f"{node_name}.INPUT_TYPES() must return a dict"
            assert (
                "required" in input_types
            ), f"{node_name}.INPUT_TYPES() must have 'required' key"

    def test_function_method_exists(self, all_nodes):
        """Test that the function method specified in FUNCTION exists."""
        for node_name, node_class in all_nodes.items():
            function_name = node_class.FUNCTION
            assert hasattr(
                node_class, function_name
            ), f"{node_name} missing function method: {function_name}"

    def test_node_instantiation(self, all_nodes):
        """Test that all nodes can be instantiated."""
        for node_name, node_class in all_nodes.items():
            instance = node_class()
            assert instance is not None, f"{node_name} failed to instantiate"


class TestSamplerSelector:
    """Test SamplerSelector node functionality."""

    def test_select_sampler(self, sampler_selector):
        """Test sampler selection."""
        result = sampler_selector.select_sampler("euler")
        assert result == ("euler",)

    def test_input_types(self, sampler_selector):
        """Test input types structure."""
        input_types = sampler_selector.INPUT_TYPES()
        assert "sampler_name" in input_types["required"]

    def test_return_types(self, sampler_selector):
        """Test return types."""
        assert len(sampler_selector.RETURN_TYPES) == 1
        assert isinstance(sampler_selector.RETURN_TYPES[0], list)

    def test_category(self, sampler_selector):
        """Test node category."""
        assert sampler_selector.CATEGORY == "Selectors/Sampling"


class TestSchedulerSelector:
    """Test SchedulerSelector node functionality."""

    def test_select_scheduler(self, scheduler_selector):
        """Test scheduler selection."""
        result = scheduler_selector.select_scheduler("karras")
        assert result == ("karras",)

    def test_input_types(self, scheduler_selector):
        """Test input types structure."""
        input_types = scheduler_selector.INPUT_TYPES()
        assert "scheduler" in input_types["required"]

    def test_category(self, scheduler_selector):
        """Test node category."""
        assert scheduler_selector.CATEGORY == "Selectors/Sampling"


class TestSeedGenerator:
    """Test SeedGenerator node functionality."""

    def test_generate_seed_fixed(self, seed_generator):
        """Test fixed seed generation."""
        result = seed_generator.generate_seed(42, "fixed")
        assert result == (42,)

    def test_generate_seed_increment(self, seed_generator):
        """Test increment seed generation."""
        result = seed_generator.generate_seed(42, "increment")
        assert result == (43,)

    def test_generate_seed_randomize(self, seed_generator):
        """Test random seed generation."""
        result = seed_generator.generate_seed(42, "randomize")
        assert isinstance(result[0], int)
        assert result[0] != 42  # Should be different from input

    def test_category(self, seed_generator):
        """Test node category."""
        assert seed_generator.CATEGORY == "Selectors/Generation"


class TestWidthNode:
    """Test WidthNode functionality."""

    def test_custom_width(self, width_node):
        """Test custom width selection."""
        result = width_node.get_width(512, "custom")
        assert result == (512,)

    def test_preset_width(self, width_node):
        """Test preset width selection."""
        result = width_node.get_width(512, "1024")
        assert result == (1024,)

    def test_category(self, width_node):
        """Test node category."""
        assert width_node.CATEGORY == "Selectors/Dimensions"


class TestHeightNode:
    """Test HeightNode functionality."""

    def test_custom_height(self, height_node):
        """Test custom height selection."""
        result = height_node.get_height(512, "custom")
        assert result == (512,)

    def test_preset_height(self, height_node):
        """Test preset height selection."""
        result = height_node.get_height(512, "768")
        assert result == (768,)

    def test_category(self, height_node):
        """Test node category."""
        assert height_node.CATEGORY == "Selectors/Dimensions"


class TestWidthHeightNode:
    """Test WidthHeightNode functionality."""

    def test_custom_dimensions(self, width_height_node):
        """Test custom dimensions."""
        result = width_height_node.get_dimensions(512, 768, "custom", False)
        assert result == (512, 768)

    def test_preset_dimensions(self, width_height_node):
        """Test preset dimensions."""
        result = width_height_node.get_dimensions(512, 768, "1024x768", False)
        assert result == (1024, 768)

    def test_swap_dimensions(self, width_height_node):
        """Test dimension swapping."""
        result = width_height_node.get_dimensions(512, 768, "custom", True)
        assert result == (768, 512)

    def test_category(self, width_height_node):
        """Test node category."""
        assert width_height_node.CATEGORY == "Selectors/Dimensions"
