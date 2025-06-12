from nodes import MAX_RESOLUTION


class HeightNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
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
                        "512",
                        "768",
                        "1024",
                        "1152",
                        "1216",
                        "1344",
                        "1408",
                        "1472",
                        "1536",
                    ],
                    {
                        "default": "custom",
                        "tooltip": "Common height presets for quick selection",
                    },
                ),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("height",)
    FUNCTION = "get_height"
    CATEGORY = "comfyassets/Dimensions"

    def get_height(self, height, preset):
        """Get height value, using preset if not custom."""
        if preset != "custom":
            height = int(preset)
        return (height,)
