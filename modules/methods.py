from .definition import REGION_TO_CODE


def get_region_code(region_name: str) -> str:
    try:
        return REGION_TO_CODE[region_name]
    except KeyError:
        return "error"
