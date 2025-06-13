#!/usr/bin/env python3
"""
Test script to verify seed tracking functionality
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "nodes"))

from random_value_tracker import SeedHistory  # noqa: E402


def test_seed_tracking():
    """Test the basic seed tracking functionality"""
    print("Testing SeedHistory node...")

    # Test node creation
    seed_node = SeedHistory()
    print("✅ SeedHistory node created successfully")

    # Test basic functionality
    result = seed_node.output_seed(12345)
    assert result == (12345,), f"Expected (12345,), got {result}"
    print("✅ Basic seed output working")

    # Test with different seed values
    test_seeds = [0, 1, 42, 123456789, 0xFFFFFFFFFFFFFFFF]
    for seed in test_seeds:
        result = seed_node.output_seed(seed)
        assert result == (seed,), f"Expected ({seed},), got {result}"
    print("✅ Multiple seed values working")

    # Test node structure
    assert hasattr(seed_node, "INPUT_TYPES"), "Missing INPUT_TYPES method"
    assert hasattr(seed_node, "RETURN_TYPES"), "Missing RETURN_TYPES"
    assert hasattr(seed_node, "RETURN_NAMES"), "Missing RETURN_NAMES"
    assert hasattr(seed_node, "FUNCTION"), "Missing FUNCTION"
    assert hasattr(seed_node, "CATEGORY"), "Missing CATEGORY"
    print("✅ Node structure is correct")

    # Test input types
    input_types = SeedHistory.INPUT_TYPES()
    assert "required" in input_types, "Missing required inputs"
    assert "seed" in input_types["required"], "Missing seed input"
    seed_config = input_types["required"]["seed"]
    assert seed_config[0] == "INT", "Seed should be INT type"
    assert "default" in seed_config[1], "Missing default value"
    assert "min" in seed_config[1], "Missing min value"
    assert "max" in seed_config[1], "Missing max value"
    print("✅ Input types configuration is correct")

    print("\n🎉 All seed tracking tests passed!")


if __name__ == "__main__":
    test_seed_tracking()
