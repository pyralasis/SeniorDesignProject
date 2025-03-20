from dataclasses import dataclass

import pydantic
from quart import Quart, jsonify, request
from server.params import AnyParameterValue, Size2DParameter, Size2DParameterValue
from server.util.file.meta import MetaData


@dataclass
class NodeConfig:
    x: AnyParameterValue


adapter = pydantic.TypeAdapter(NodeConfig)

print(
    adapter.validate_json(
        """{
    "x": { "type": "size2d", "val": ["1", "2"]}
}"""
    )
)

# app = Quart(__name__)


# @app.route("/validate", methods=["POST"])
# async def validate():
#     data = await request.get_data()
#     print(type(data), data)
#     try:
#         validated_data = adapter.validate_json(data)
#         return jsonify(validated_data), 200
#     except pydantic.ValidationError as e:
#         return {"msg": "invalid"}, 400


# if __name__ == "__main__":
#     app.run()
