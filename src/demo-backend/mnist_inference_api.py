"""
Provide a simple API for inference of MNIST model.

Command line arguments:
    --port: port to run the server on
    --weight_path: path to the model weights file

Example usage:
    python mnist_inference_api.py --port 8888 --weight_path mnist_cnn.pt

API endpoints:
    GET /api/demo/infer
        Query parameters:
            image: list of lists of floats representing the image
        Returns:
            prediction: int representing the predicted digit
"""

import argparse
import logging
import torch
import torch.nn as nn
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import numpy as np
from mnist_demo_pt import Net
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define request model
class InferenceRequest(BaseModel):
    image: list[list[float]]

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

@app.post("/api/demo/infer")
async def infer(request: InferenceRequest):
    try:
        # Convert to numpy array and validate dimensions
        image_array = np.array(request.image)
        if image_array.shape != (28, 28):
            raise HTTPException(status_code=400, detail="Image must be 28x28")
        
        # validate values
        if np.any(image_array < MIN_VAL) or np.any(image_array > MAX_VAL):
            raise HTTPException(status_code=400, detail="Image values must be between 0 and 255")
        
        # Convert to tensor and add batch and channel dimensions
        image_tensor = torch.FloatTensor(image_array).unsqueeze(0).unsqueeze(0)
        
        # Run inference
        with torch.no_grad():
            output = model(image_tensor)
            prediction = output.argmax(dim=1).item()
        
        logger.info(f"Inference completed. Prediction: {prediction}")
        return {"prediction": prediction}
    
    except Exception as e:
        logger.error(f"Error during inference: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def load_model(weight_path: str):
    global model
    try:
        model = Net()
        model.load_state_dict(torch.load(weight_path))
        model.eval()
        logger.info(f"Model loaded successfully from {weight_path}")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description="MNIST Inference API Server")
    parser.add_argument("--port", type=int, default=8888, help="Port to run the server on")
    parser.add_argument("--weight_path", type=str, required=True, help="Path to the model weights file")
    args = parser.parse_args()

    # Load model
    load_model(args.weight_path)

    # Start server
    uvicorn.run(app, host="0.0.0.0", port=args.port)

if __name__ == "__main__":
    main() 