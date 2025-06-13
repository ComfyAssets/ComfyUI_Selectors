class SeedHistory:
    """A seed node with history tracking capabilities."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": (
                    "INT",
                    {
                        "default": 12345,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "tooltip": "Seed value for generation processes",
                    },
                ),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)
    FUNCTION = "output_seed"
    CATEGORY = "comfyassets/Generation"

    def output_seed(self, seed):
        """Output the seed value for use in other nodes."""
        return (seed,)
