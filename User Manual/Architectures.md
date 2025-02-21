# Architectures

# What is an Architecture

An Architecture is the sum of a Neural Network's Layers, Parameters and Shape.

A Layer is the main componenent that an Architecture is built out of. Each Layer has a set of parameters. The Shape describes how the Layers are connected to eachother adn how data flows through the Architecture.

## Selecting an Architecture

Click 'Select Architecture' via the 'Architectures' button on the navigation bar. Once on the 'Select Architecture' page you can create a new Architecture or you can select an existing one. 

## Using the Architecture Editor

You can create and edit your Architecture through the Architecture Node Editor. The sidebar contains the available Layer types you can use to construct your Architecture. The Editor allows you to drag a Layer and drop it into the Editor.

Once a Layer is in the Editor, you can connect it to other Layers and edit its Parameters.

## Supported Layer Types
Provided are links to the Pytorch documentation for each Layer type.

- [ReLu](https://pytorch.org/docs/stable/generated/torch.nn.ReLU.html)
- [2D Convolution](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html#torch.nn.Conv2d)
- [Linear](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html#torch.nn.Linear)
- [2D Max Pooling](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html#torch.nn.MaxPool2d)