import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() # import env vars
import numpy as np

client = OpenAI(
    base_url = os.getenv('BASE_URL') , #ollama running hai iss jagah pe
    api_key = os.getenv('API_KEY')
)

EMBED_MODEL= os.getenv('EMBED_MODEL')
KNOWLEDGE_BASE_FOLDER = os.getenv('KNOWLEDGE_BASE')
VECTOR_STORE_LOC = os.getenv("VECTOR_STORE_FILE")

# 2 super pvt methods
def generate_embeddings(text_list):
    response = client.embeddings.create(
        model= EMBED_MODEL,
        input=text_list
    )

    #Abhi response me arr of object hai text + 

    embeddings_list = []
    for items in response.data :
        embeddings_list.append(items.embedding)

    return embeddings_list
def cosine_similarity(vec1 ,vec2):
    dot_prod = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)

    denominator = norm_a * norm_b
    if denominator == 0 : 
            return [0.0]
    return dot_prod / (norm_a * norm_b)

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

#searching topk similar docs
def search_top_k_similar_chunk(query, chunks, k=3):

    query_vector = generate_embeddings(query)

    results = []
    for chunk in chunks:
        score = cosine_similarity(query_vector, chunk["vector"])
        results.append({
            "score" : score,
            "source":chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "text":chunk["text"],
            "size" : len(chunk["text"])
        })  

    results.sort(key=lambda doc : doc["score"], reverse=True)
    return results[:k]

def test_search(user_query, chunks, k = 3):
    print("User Query: ", user_query)

    results = search_top_k_similar_chunk(user_query, chunks, k)
    # print(results)
    for res in results:
        print()
        print(f"Score: {res['score'][0]:.2f}, Source: {res['source']}, Size: {res['size']}")
        print(res["text"])
      

def create_chunks():
    documents = load_all_files_from_folder();
    chunk = []

    # print("Splitted : ", documents[0]["text"].split("\n\n"))
    for doc in documents:
        chunk.extend(chunk_this_doc(doc)) # list me list of chunks daalta hai 
    return chunk

def chunk_this_doc(document):
    parts = []
    chunks = []
    chunk_id = 0

    partitioned_doc = document["text"].split("\n\n")

    for part in partitioned_doc:
        part = part.strip()
        
        if part: 
            parts.append(part);
            
        if len(parts) == 5:
            vectorized_chunks = generate_embeddings(parts);
            i = 0
            for vector in vectorized_chunks : 
                chunks.append({
                            "source": document["source"],
                            "chunk_id" : chunk_id,
                            "text" : parts[i],
                            "vector" : vector
                        })
                i+= 1
                chunk_id += 1


            parts = []

    # Agr kuch reh gya hai aur parts kaa length 5 nhi hora hai to ye
    if parts:
        vectorized_chunks = generate_embeddings(parts);
        i = 0
        for vector in vectorized_chunks : 
            chunks.append({
                        "source": document["source"],
                        "chunk_id" : chunk_id,
                        "text" : parts[i],
                        "vector" :vector,
                    })
            i+= 1
            chunk_id += 1

        parts = []

    return chunks



def save_vector_store(chunks): #hoga nhi to bnaega likhne ke liye
    with open(VECTOR_STORE_LOC, "w", encoding="utf-8") as f :
        json.dump(chunks, f, indent=4, allow_nan=False)

def load_vector_store():  #loads from there
    with open(VECTOR_STORE_LOC, "r", encoding="utf-8") as f :
        return json.load(f)


chunks = []

if os.path.exists(VECTOR_STORE_LOC): #AGAR PAHLE SE HAI MATLB VECTOR_STORE BNA HAI ELSE NHI HAI 
    chunks = load_vector_store();
    print(f"we have used {len(chunks)} chunks (ALREADY_SAVED) " )
else:
    chunks = create_chunks()
    save_vector_store(chunks) 
    print("created for first ☻time")


# chunks = create_chunks()ss


user_query = "what are benefits of sick leaves and coverages of it"
test_search(user_query, chunks, k = 3)