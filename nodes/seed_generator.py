import random


class SeedGenerator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "tooltip": "Seed value for reproducible generation. Use 0 with randomize for random seeds.",  # noqa: E501
                    },
                ),
                "control_after_generate": (
                    ["fixed", "increment", "decrement", "randomize"],
                    {
                        "default": "randomize",
                        "tooltip": "How to handle seed after generation",
                    },
                ),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)
    FUNCTION = "generate_seed"
    CATEGORY = "comfyassets/Generation"

    def generate_seed(self, seed, control_after_generate):
        """Generate and return seed value for use in other nodes."""
        if control_after_generate == "randomize":
            seed = random.randint(0, 0xFFFFFFFFFFFFFFFF)
        elif control_after_generate == "increment":
            seed = (seed + 1) % (0xFFFFFFFFFFFFFFFF + 1)
        elif control_after_generate == "decrement":
            seed = (seed - 1) % (0xFFFFFFFFFFFFFFFF + 1)
        # "fixed" mode returns the seed as-is

        return (seed,)
