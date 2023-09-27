"""
model download and reuse class
"""
from sentence_transformers import SentenceTransformer
import os

class SentenceTransformerLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = cls._load_sentence_transformer_model()
        return cls._instance

    @staticmethod
    def _load_sentence_transformer_model():
        model_dir = "SenTransformCache\model_cache"
        model_name = "multi-qa-distilbert-cos-v1"  
        model_path = os.path.join(model_dir, model_name)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model '{model_name}' not found in cache")

        # Load the Sentence Transformer model
        model = SentenceTransformer(model_path)

        return model

    def get_model(self):
        return self._model
