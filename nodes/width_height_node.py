from nodes import MAX_RESOLUTION


class WidthHeightNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": (
                    "INT",
                    {
                        "default": 512,
                        "min": 64,
                        "max": MAX_RESOLUTION,
                        "step": 8,
                        "tooltip": "Image width in pixels (must be multiple of 8)",
                    },
                ),
                "height": (
                    "INT",
                    {
                        "default": 512,
                        "min": 64,
                        "max": MAX_RESOLUTION,
                        "step": 8,
                        "tooltip": "Image height in pixels (must be multiple of 8)",
                    },
                ),
                "preset": (
                    [
                        "custom",
                        "512x512",
                        "768x512",
                        "1024x768",
                        "1152x896",
                        "1216x832",
                        "1344x768",
                        "1408x704",
                        "1472x704",
                        "1536x640",
                        "640x1536",
                        "704x1472",
                        "704x1408",
                        "768x1344",
                        "832x1216",
                        "896x1152",
                        "768x1024",
                        "512x768",
                    ],
                    {
                        "default": "custom",
                        "tooltip": "Common dimension presets for quick selection",
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
        if preset != "custom":
            preset_parts = preset.split("x")
            width = int(preset_parts[0])
            height = int(preset_parts[1])

        if swap_dimensions:
            width, height = height, width

        return (width, height)
