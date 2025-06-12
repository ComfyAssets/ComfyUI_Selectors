import comfy.samplers


class SchedulerSelector:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "scheduler": (
                    comfy.samplers.KSampler.SCHEDULERS,
                    {
                        "default": "normal",
                        "tooltip": "The scheduler algorithm to control sampling step distribution",  # noqa: E501
                    },
                ),
            }
        }

    RETURN_TYPES = (comfy.samplers.KSampler.SCHEDULERS,)
    RETURN_NAMES = ("scheduler",)
    FUNCTION = "select_scheduler"
    CATEGORY = "comfyassets/Sampling"

    def select_scheduler(self, scheduler):
        """Select and return scheduler name for use in other nodes."""
        return (scheduler,)
