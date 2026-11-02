import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() # import env vars
import numpy as np

client = OpenAI(
    base_url = os.getenv('BASE_URL') , #ollama running hai iss jagah pe
    api_key = os.getenv('API_KEY')
)

EMBED_MODEl= os.getenv('EMBED_MODEL')
KNOWLEDGE_BASE_FOLDER = os.getenv('KNOWLEDGE_BASE')


# loading all files
def load_all_files_from_folder(folder = KNOWLEDGE_BASE_FOLDER):

    documents = []
    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"): 
            continue

        filepath = os.path.join(folder, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            documents.append({
                "source":filename,
                "text": file.read()

            })

    return documents




# 2 super pvt methods
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


#adding embeddinngs in the docs
def add_embeddings_to_documents(documents):

    for doc in documents:
        vector = generate_embeddings(doc["text"])
        doc["vector"] = vector

    return documents

#searching topk similar docs

def search_top_k_similar_documents(query, documents, k=3):

    query_vector = generate_embeddings(query)
    results = []
    for doc in documents:
        score = cosine_similarity(query_vector, doc["vector"])
        results.append({
            "score" : score,
            "source":doc["source"],
            "text":doc["text"],
            "size" : len(doc["text"])
        })  

    results.sort(key=lambda doc : doc["score"], reverse=True)
    return results[:k]

def test_search(user_query, documents, k = 3):
    print("User Query: ", user_query)

    results = search_top_k_similar_documents(user_query, documents, k)

    for res in results:
        print(f"Score: {res['score']:.2f}, Source: {res['source']}, Size: {res['size']}")


documents = load_all_files_from_folder(KNOWLEDGE_BASE_FOLDER)
documnents_with_embeddings = add_embeddings_to_documents(documents)

print(f"we have embedded {len(documents)} documents" )

user_query = "How many days I will get for maternity leave ? "
test_search(user_query, documnents_with_embeddings, k = 3)