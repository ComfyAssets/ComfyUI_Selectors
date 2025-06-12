"""
Integration tests that simulate ComfyUI workflow scenarios.
"""

import pytest  # noqa: F401


class TestWorkflowIntegration:
    """Test nodes working together in workflow scenarios."""

    def test_sampling_workflow(
        self, sampler_selector, scheduler_selector, seed_generator
    ):
        """Test a typical sampling workflow with selector nodes."""
        # Select sampler
        sampler_result = sampler_selector.select_sampler("euler")
        assert sampler_result == ("euler",)

        # Select scheduler
        scheduler_result = scheduler_selector.select_scheduler("karras")
        assert scheduler_result == ("karras",)

        # Generate seed
        seed_result = seed_generator.generate_seed(42, "fixed")
        assert seed_result == (42,)

        # Verify all outputs are tuples (ComfyUI format)
        assert isinstance(sampler_result, tuple)
        assert isinstance(scheduler_result, tuple)
        assert isinstance(seed_result, tuple)

    def test_dimension_workflow(self, width_node, height_node, width_height_node):
        """Test a typical dimension workflow with selector nodes."""
        # Set width
        width_result = width_node.get_width(512, "1024")
        assert width_result == (1024,)

        # Set height
        height_result = height_node.get_height(768, "custom")
        assert height_result == (768,)

        # Set both dimensions
        both_result = width_height_node.get_dimensions(512, 768, "1024x768", False)
        assert both_result == (1024, 768)

        # Test dimension swapping
        swapped_result = width_height_node.get_dimensions(512, 768, "custom", True)
        assert swapped_result == (768, 512)

    def test_all_nodes_together(self, all_nodes):
        """Test that all nodes can work together without conflicts."""
        instances = {}

        # Instantiate all nodes
        for node_name, node_class in all_nodes.items():
            instances[node_name] = node_class()

        # Test that they all have unique categories or share appropriately
        categories = {instance.CATEGORY for instance in instances.values()}
        expected_categories = {
            "Selectors/Sampling",
            "Selectors/Generation",
            "Selectors/Dimensions",
        }
        assert categories == expected_categories

        # Test that all function methods are callable
        for node_name, instance in instances.items():
            function_name = instance.FUNCTION
            function_method = getattr(instance, function_name)
            assert callable(function_method)

    def test_node_output_compatibility(self, all_nodes):
        """Test that all node outputs are in ComfyUI-compatible format."""
        test_cases = {
            "SamplerSelector": ("euler",),
            "SchedulerSelector": ("karras",),
            "SeedGenerator": (42, "fixed"),
            "WidthNode": (512, "custom"),
            "HeightNode": (512, "custom"),
            "WidthHeightNode": (512, 768, "custom", False),
        }

        for node_name, test_args in test_cases.items():
            node_class = all_nodes[node_name]
            instance = node_class()
            function_name = instance.FUNCTION
            function_method = getattr(instance, function_name)

            result = function_method(*test_args)

            # All results should be tuples (ComfyUI format)
            assert isinstance(result, tuple)
            assert len(result) >= 1
