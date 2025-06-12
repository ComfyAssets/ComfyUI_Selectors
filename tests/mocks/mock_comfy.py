"""
Mock ComfyUI modules for testing purposes.
"""


# Mock comfy.samplers module
class MockKSampler:
    SAMPLERS = [
        "euler",
        "euler_ancestral",
        "heun",
        "heunpp2",
        "dpm_2",
        "dpm_2_ancestral",
        "lms",
        "dpm_fast",
        "dpm_adaptive",
        "dpmpp_2s_ancestral",
        "dpmpp_sde",
        "dpmpp_sde_gpu",
        "dpmpp_2m",
        "dpmpp_2m_sde",
        "dpmpp_2m_sde_gpu",
        "dpmpp_3m_sde",
        "dpmpp_3m_sde_gpu",
        "ddpm",
        "lcm",
        "ddim",
        "uni_pc",
        "uni_pc_bh2",
    ]

    SCHEDULERS = [
        "normal",
        "karras",
        "exponential",
        "sgm_uniform",
        "simple",
        "ddim_uniform",
        "beta",
    ]


class MockSamplers:
    KSampler = MockKSampler


# Mock nodes module
MAX_RESOLUTION = 8192

# Mock random module (using real one)
import random  # noqa: F401, E402
