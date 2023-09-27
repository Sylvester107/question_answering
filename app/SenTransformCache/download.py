'''
run this script to download and save the transformer model once

'''
from sentence_transformers import SentenceTransformer
import os

model_name = "multi-qa-distilbert-cos-v1"  # QA model name
cache_dir = "model_cache"

# Ensure the cache directory exists
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

model_path = os.path.join(cache_dir, model_name)

if not os.path.exists(model_path):
    # Download the model if it doesn't exist in the cache
    model = SentenceTransformer(model_name)

    # Save the downloaded model to the cache
    model.save(model_path)
