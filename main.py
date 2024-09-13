import json
import urllib.request
from transformers import AutoModelForImageClassification, AutoFeatureExtractor, pipeline
from PIL import Image
import requests
import torch
import urllib
from torchvision import transforms, datasets
import random
import numpy as np
import os
import time

model = AutoModelForImageClassification.from_pretrained('model')


def predict(image_path, classLabels):
    try:
        data_transforms = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

        image = Image.open(urllib.request.urlopen(image_path))
        image = data_transforms(image).unsqueeze(0)

        # Predict the class
        with torch.no_grad():
            outputs = model(image)
            predictions = torch.argmax(outputs.logits, dim=1)

        # Convert prediction to class label
        idx_to_class = {v: k for k, v in classLabels.items()}
        prediction = idx_to_class[predictions.item()]

        return {
            "Message": "Success",
            "Prediction": prediction
        }
    except Exception as e:
        return {
            "Message": "Error Occurred",
            "Error": str(e)
        }


def makePrediction(image_url):
    with open('model/classnames.json', 'r') as f:
        classLabels = json.load(f)
        f.close()
    return predict(image_url, classLabels)
