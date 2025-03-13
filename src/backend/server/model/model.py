import torch
from server.architecture.config import (
    ArchitectureConfig,
    LayerInstanceID,
    NetworkLayerConfig,
)
from server.layer.service import LayerService
from server.layer.size import TensorSize


class ArchitectureExecutionInfo:
    def __init__(self, input_ids: list[LayerInstanceID], out_id: LayerInstanceID) -> None:
        self.layers = torch.nn.ModuleDict()
        self.input_map: dict[str, list[str]] = {}

        self.input_ids = [str(id) for id in input_ids]
        self.out_id = str(out_id)

    def add_layer(self, id: LayerInstanceID, layer: torch.nn.Module, inputs: list[LayerInstanceID]):
        """Adds layer to the execution info. This is a ordered operation (the first added will be the first layer to run)."""
        id_str = str(id)
        self.layers.add_module(id_str, layer)
        self.input_map[id_str] = [str(input) for input in inputs]


class ArchitectureModel(torch.nn.Module):
    def __init__(self, exec_info: ArchitectureExecutionInfo) -> None:
        super(ArchitectureModel, self).__init__()

        self.layers = exec_info.layers
        self.input_map = exec_info.input_map

        self.input_ids = exec_info.input_ids
        self.out_id = exec_info.out_id

    def forward(self, data: list[torch.Tensor]):
        data_cache = {in_id: data[i] for i, in_id in enumerate(self.input_ids)}

        for layer_instance_id, layer in self.layers.items():
            input_data = [data_cache[input] for input in self.input_map[layer_instance_id]]
            data_cache[layer_instance_id] = layer(*input_data)

        return data_cache[self.out_id]

    @staticmethod
    def create_from_architecture(architecture: ArchitectureConfig, layer_service: LayerService):
        arch_inputs = [input.instance_id for input in architecture.inputs]
        arch_output = architecture.output

        layers: dict[LayerInstanceID, NetworkLayerConfig] = {  # id to layer configuration
            layer.instance_id: layer for layer in architecture.layers
        }

        # used in the transform function
        output_size: dict[LayerInstanceID, TensorSize] = {  # output sizes of the layers
            input.instance_id: input.size for input in architecture.inputs  # start with the input sizes prepopulated
        }

        # recursive function to construct the layers
        # base case is when the layer is an input, the output size will already be in the output_size dict
        # recursive case is when the layer is a network layer
        def construct_layers(instance_id: LayerInstanceID, exec_info: ArchitectureExecutionInfo) -> None:
            if instance_id in arch_inputs:  # No need to construct an input, TODO: make set for faster check?
                return

            layer_instance = layers[instance_id]  # get the layer instance
            layer_definition = layer_service.layers.get(layer_instance.layer_id)  # get the layer definition
            input_sizes: list[TensorSize] = []  # input sizes of the current layer

            # iterate the inputs of the current layer
            for input_id in layer_instance.input:
                # if the input is not in the layer_output_sizes, construct the layers
                if input_id not in output_size:
                    construct_layers(input_id, exec_info)

                input_sizes.append(output_size[input_id])

            # construct the layer and set the output size
            layer_module = layer_definition.constructor(tuple(input_sizes), **layer_instance.get_params())
            output_size[instance_id] = layer_definition.size(tuple(input_sizes), **layer_instance.get_params())

            exec_info.add_layer(instance_id, layer_module, layer_instance.input)

        exec_info = ArchitectureExecutionInfo(arch_inputs, arch_output)
        construct_layers(arch_output, exec_info)

        return ArchitectureModel(exec_info)
