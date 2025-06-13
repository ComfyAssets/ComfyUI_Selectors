from .nodes.height_node import HeightNode
from .nodes.random_value_tracker import SeedHistory
from .nodes.sampler_selector import SamplerSelector
from .nodes.scheduler_selector import SchedulerSelector
from .nodes.width_height_node import WidthHeightNode
from .nodes.width_node import WidthNode

# Print startup message in blue
print("\033[94m [ComfyAssets Selectors] Loaded..\033[0m")

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "SamplerSelector": SamplerSelector,
    "SchedulerSelector": SchedulerSelector,
    "SeedHistory": SeedHistory,
    "WidthNode": WidthNode,
    "HeightNode": HeightNode,
    "WidthHeightNode": WidthHeightNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SamplerSelector": "Sampler Selector",
    "SchedulerSelector": "Scheduler Selector",
    "SeedHistory": "Seed History",
    "WidthNode": "Width",
    "HeightNode": "Height",
    "WidthHeightNode": "Width & Height",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
