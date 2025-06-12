WEB_DIRECTORY = "./web"

from .nodes.height_node import HeightNode
from .nodes.sampler_selector import SamplerSelector
from .nodes.scheduler_selector import SchedulerSelector
from .nodes.seed_generator import SeedGenerator
from .nodes.width_height_node import WidthHeightNode
from .nodes.width_node import WidthNode

NODE_CLASS_MAPPINGS = {
    "SamplerSelector": SamplerSelector,
    "SchedulerSelector": SchedulerSelector,
    "SeedGenerator": SeedGenerator,
    "WidthNode": WidthNode,
    "HeightNode": HeightNode,
    "WidthHeightNode": WidthHeightNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SamplerSelector": "Sampler Selector",
    "SchedulerSelector": "Scheduler Selector",
    "SeedGenerator": "Seed Generator",
    "WidthNode": "Width",
    "HeightNode": "Height",
    "WidthHeightNode": "Width & Height",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
