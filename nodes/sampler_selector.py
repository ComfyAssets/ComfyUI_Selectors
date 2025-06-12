import comfy.samplers


class SamplerSelector:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sampler_name": (
                    comfy.samplers.KSampler.SAMPLERS,
                    {
                        "default": "euler",
                        "tooltip": "The sampling algorithm to use for generation",
                    },
                ),
            }
        }

    RETURN_TYPES = (comfy.samplers.KSampler.SAMPLERS,)
    RETURN_NAMES = ("sampler_name",)
    FUNCTION = "select_sampler"
    CATEGORY = "comfyassets/Sampling"

    def select_sampler(self, sampler_name):
        """Select and return sampler name for use in other nodes."""
        return (sampler_name,)
