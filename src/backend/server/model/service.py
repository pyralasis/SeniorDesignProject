import uuid
from ast import Mod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from server.architecture.config import (
    ArchitectureConfig,
    InputLayerConfig,
    LayerInstanceID,
    NetworkLayerConfig,
)
from server.layer import LayerDefinition
from server.layer.service import LayerService
from server.layer.size import TensorSize
from server.util.file import Loadable, MetaData, TorchWeightsFileManager
from server.util.file.coordinator import FileCoordinator

"""
Sample model architecture:
{
    "name": "Example Architecture",
    "version": 1,
    "inputs": [{"id":1,"size":[10]}],
    "layers": [
        {"id":2,"layer_id":"linear","input":1,"param_values":{"out_features":{"val":5,"type":"int"},"bias":{"val":true,"type":"bool"}}},
        {"id":3,"layer_id":"linear","input":2,"param_values":{"out_features":{"val":1,"type":"int"},"bias":{"val":true,"type":"bool"}}}
    ],
    "layout_file": null
}
"""


@dataclass
class ModelObject(Loadable):
    meta: MetaData
    data: dict[str, Any]  # the model's state_dict


class ModelService:
    """
    A service for managing PyTorch models.
    """

    def __init__(self, layer_service: LayerService, save_path: Path) -> None:
        self.layer_service = layer_service
        self.models = FileCoordinator(
            ModelObject,
            "model",
            TorchWeightsFileManager("data", save_path, ".pt"),
            [],
            save_path,
        )

    # TODO
    # - create the model from the architecture
    # - save the model to the file system
    # - return the model_id
    def create_model(self, architecture: ArchitectureConfig, meta_data: MetaData) -> str:
        # Stub
        arch_inputs: list[InputLayerConfig] = architecture.inputs
        arch_output: LayerInstanceID = architecture.output
        arch_layers: list[NetworkLayerConfig] = architecture.layers

        # used in the transform function
        layer_output_sizes: dict[LayerInstanceID, TensorSize] = {}  # output sizes of the layers
        arch_inputs_ids: dict[LayerInstanceID, InputLayerConfig] = {
            input.instance_id: input for input in arch_inputs
        }  # input layer ids
        layer_instances: dict[LayerInstanceID, NetworkLayerConfig] = {
            layer.instance_id: layer for layer in arch_layers
        }  # layer instances

        # the layers that are created
        created_layers: dict[LayerInstanceID, torch.nn.Module] = {}  # created layers

        # recursive function to construct the layers
        # base case is when the layer is an input
        # recursive case is when the layer is a network layer
        # the recursive case should call the base case
        def construct_layers(instance_id: LayerInstanceID) -> None:
            # if the layer is an input, set the output size and return
            if instance_id in arch_inputs_ids:
                layer_output_sizes[instance_id] = arch_inputs_ids[instance_id].size
                return

            # if the layer is a network layer, construct the layers
            layer_instance = layer_instances[instance_id]  # get the layer instance
            layer_definition = self.layer_service.layers.get(layer_instance.layer_id)  # get the layer definition
            input_sizes: list[TensorSize] = []  # input sizes of the current layer

            # iterate the inputs of the current layer
            for input_id in layer_instance.input:
                # if the input is not in the layer_output_sizes, construct the layers
                if input_id not in layer_output_sizes:
                    construct_layers(input_id)
                input_sizes.append(layer_output_sizes[input_id])

            # construct the layer and set the output size
            layer_module = layer_definition.constructor(tuple(input_sizes), **layer_instance.get_params())
            layer_output_sizes[instance_id] = layer_definition.size(tuple(input_sizes), **layer_instance.get_params())
            created_layers[instance_id] = layer_module

        construct_layers(arch_output)

        # now we have the created layers organized by instance id
        # we can now create the model
        model = torch.nn.Sequential(*created_layers.values())

        # make the model id
        model_id = str(uuid.uuid1())

        # save the model to the file system
        self.models.create(ModelObject(meta_data, model.state_dict()))

        # return the model id
        return model_id
