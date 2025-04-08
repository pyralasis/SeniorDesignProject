"""
Provide a simple API for inference of MNIST model.

Command line arguments:
    --port: port to run the server on

Example usage:
    python mnist_inference_api.py --port 8888

API endpoints:
    GET /api/demo/infer
        Query parameters:
            image: list of lists of floats representing the image
        Returns:
            prediction: int representing the predicted digit
"""

import argparse
import logging
from pathlib import Path
from typing import Optional

import PIL.Image
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mnist_demo_pt import Net
from pydantic import BaseModel
from server.architecture.service import ArchitectureService
from server.data.service import DataService
from server.data.sources import default_sources
from server.data.transforms import default_transforms
from server.layer.definitions import default_layers
from server.layer.service import LayerService
from server.model.service import ModelService
from server.util.file.file import FileId
from server.util.file.object import ObjectDescription
from torchvision import datasets, transforms


transform=transforms.Compose([
        transforms.Normalize((0.1307,), (0.3081,))
        ])

layer_service = LayerService(default_layers)
data_service = DataService(Path("./"), default_sources, default_transforms)
architecture_service = ArchitectureService(Path("./"))
model_service = ModelService(layer_service, data_service, architecture_service, Path("../backend/models"), Path("./"))


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


MAX_VAL = 255
MIN_VAL = 0

# Initialize FastAPI app
app = FastAPI(title="MNIST Inference API")

origins = [
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5173",
    "http://localhost:5176",
    "http://localhost:5177",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None


@app.get("/api/demo/available_models")
async def available_models():
    try:
        # Get available models
        available_models: list[ObjectDescription] = model_service.models.available()
        logger.info(f"Available models: {available_models}")
        return available_models
    except Exception as e:
        logger.error(f"Error fetching available models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Define request model
class LoadModelRequest(BaseModel):
    id: FileId


@app.post("/api/demo/load_model")
async def load_model(request: LoadModelRequest):
    global model
    try:
        # Load model
        model = model_service.load_model(request.id)
        logger.info(f"Model loaded successfully: {request.id}")
        return {"message": "Model loaded successfully"}
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Define request model
class InferenceRequest(BaseModel):
    image: list[list[float]]


@app.post("/api/demo/infer")
async def infer(request: InferenceRequest):
    try:
        if model is None:
            raise HTTPException(status_code=400, detail="Model not loaded")

        # Convert to numpy array and validate dimensions
        image_array = np.array(request.image)
        if image_array.shape != (28, 28):
            raise HTTPException(status_code=400, detail="Image must be 28x28")

        # validate values
        if np.any(image_array < MIN_VAL) or np.any(image_array > MAX_VAL):
            raise HTTPException(status_code=400, detail="Image values must be between 0 and 255")

        # import matplotlib.pyplot as plt
        # plt.imshow(image_array)
        # plt.show()

        # Convert to tensor and add batch and channel dimensions
        image_tensor = torch.FloatTensor(image_array).unsqueeze(0).unsqueeze(0)
        image_tensor = transform(image_tensor)
        # Run inference
        with torch.no_grad():
            output = model([image_tensor])
            prediction = output.argmax(dim=1).item()

        logger.info(f"Inference completed. Prediction: {prediction}")
        return {"prediction": prediction}

    except Exception as e:
        logger.error(f"Error during inference: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# def load_model(weight_path: str):
#     global model
#     try:
#         model = Net()
#         model.load_state_dict(torch.load(weight_path))
#         model.eval()
#         logger.info(f"Model loaded successfully from {weight_path}")
#     except Exception as e:
#         logger.error(f"Error loading model: {str(e)}")
#         raise


def main():
    parser = argparse.ArgumentParser(description="MNIST Inference API Server")
    parser.add_argument("--port", type=int, default=8888, help="Port to run the server on")
    # parser.add_argument("--weight_path", type=str, required=True, help="Path to the model weights file")
    args = parser.parse_args()

    # # Load model
    # load_model(args.weight_path)

    # Start server
    uvicorn.run(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
