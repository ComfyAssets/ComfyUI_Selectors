from nodes import MAX_RESOLUTION


class WidthHeightNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": (
                    "INT",
                    {
                        "default": 1024,
                        "min": 64,
                        "max": MAX_RESOLUTION,
                        "step": 8,
                        "tooltip": "Image width in pixels (must be multiple of 8)",
                    },
                ),
                "height": (
                    "INT",
                    {
                        "default": 1024,
                        "min": 64,
                        "max": MAX_RESOLUTION,
                        "step": 8,
                        "tooltip": "Image height in pixels (must be multiple of 8)",
                    },
                ),
                "preset": (
                    [
                        "custom",
                        "1024x1024",
                        "1152x896",
                        "896x1152",
                        "1216x832",
                        "832x1216",
                        "1344x768",
                        "768x1344",
                        "1536x640",
                        "640x1536",
                    ],
                    {
                        "default": "custom",
                        "tooltip": "SDXL/FLUX resolution presets",
                    },
                ),
                "swap_dimensions": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Swap width and height values"},
                ),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "get_dimensions"
    CATEGORY = "comfyassets/Dimensions"

    def get_dimensions(self, width, height, preset, swap_dimensions):
        """Get width and height values with preset and swap support."""
        # Mapping for swapped presets
        swap_mapping = {
            "1024x1024": "1024x1024",  # Square stays the same
            "1152x896": "896x1152",
            "896x1152": "1152x896",
            "1216x832": "832x1216",
            "832x1216": "1216x832",
            "1344x768": "768x1344",
            "768x1344": "1344x768",
            "1536x640": "640x1536",
            "640x1536": "1536x640",
        }

        if preset != "custom":
            if swap_dimensions and preset in swap_mapping:
                # Use the swapped preset to get proper dimensions
                swapped_preset = swap_mapping[preset]
                preset_parts = swapped_preset.split("x")
            else:
                preset_parts = preset.split("x")

            width = int(preset_parts[0])
            height = int(preset_parts[1])
        elif swap_dimensions:
            # Only swap custom dimensions
            width, height = height, width

        return (width, height)
