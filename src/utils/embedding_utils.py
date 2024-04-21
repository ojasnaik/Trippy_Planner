import openai
import numpy as np
import re

# client = openai.OpenAI()

# def get_embeddings(text, model="text-embedding-ada-002"):
#    text = text.replace("\n", " ")
#    return openai.embeddings.create(input = [text], model=model).data[0].embedding

def get_embeddings(texts):
    api_call_obj = openai.Embedding.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    obj = api_call_obj["data"][0]["embedding"]
    return obj

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)