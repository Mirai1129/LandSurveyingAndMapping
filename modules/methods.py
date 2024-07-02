from .definition import REGION_TO_CODE, CODE_TO_REGION


def get_region_code(region_name: str) -> str:
    return REGION_TO_CODE.get(region_name, "error")


def get_region_name(region_code: str) -> str:
    return CODE_TO_REGION.get(region_code, "error")
