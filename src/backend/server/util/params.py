from typing import Any, Mapping

from server.params import AnyParameterValue


def get_params_dict(values: Mapping[str, AnyParameterValue]) -> dict[str, Any]:
    return {key: param.val for key, param in values.items()}
