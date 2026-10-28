from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
import os

load_dotenv() # import env vars



def generate_embeddings(text):
    response = client.embeddings.create(
        model=os.getenv("EMBED_MODEL"),
        # input="I am a good boy"
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(vec1 ,vec2):
    dot_prod = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    return dot_prod / (norm_a * norm_b)


client  = OpenAI(
    base_url = os.getenv('BASE_URL') , #ollama running hai iss jagah pe 
    api_key = os.getenv('API_KEY')
)


text1 = "Python is a programming language"
text2 = "Python is used for web development, data analysis, and more."
text3 = "I love Samosa"


embed1 = generate_embeddings(text1)
embed2 = generate_embeddings(text2)
embed3 = generate_embeddings(text3)

similarity_score_12 = cosine_similarity(embed1, embed2)
# similarity_score_23 = cosine_similarity(embed2, embed3)
similarity_score_13 = cosine_similarity(embed1, embed3)


print(f"Similarity between text1 and text2: ",f"{similarity_score_12:.2f}")
# print(f"Similarity between text2 and text3: {similarity_score_23}")
print(f"Similarity between text1 and text3: ", f"{similarity_score_13:.2f}")