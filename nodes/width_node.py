from nodes import MAX_RESOLUTION


class WidthNode:
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
                "preset": (
                    [
                        "custom",
                        "640",
                        "768",
                        "832",
                        "896",
                        "1024",
                        "1152",
                        "1216",
                        "1344",
                        "1536",
                    ],
                    {
                        "default": "custom",
                        "tooltip": "SDXL/FLUX width presets",
                    },
                ),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("width",)
    FUNCTION = "get_width"
    CATEGORY = "comfyassets/Dimensions"

    def get_width(self, width, preset):
        """Get width value, using preset if not custom."""
        if preset != "custom":
            width = int(preset)
        return (width,)
