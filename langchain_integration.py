from neo4j import GraphDatabase
from langchain.prompts import PromptTemplate
from transformers import pipeline
from huggingface_hub import login, model_info
import faulthandler

faulthandler.enable()

from main import driver

#executes Neo4j driver's session and return records 
def query_neo4j(query):
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]


def get_movie_genre(movie_name):
    query = f"MATCH (m:Movie {{title: '{movie_name}'}}) RETURN m.genre AS genre"
    result = query_neo4j(query)
    if result:
        return result[0]["genre"]
    else:
        return "Movie not found"

#hogin to hugging face hub using token for authentication
login('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')

try:
    model_info("daryl149/llama-2-7b-hf")  
except Exception as e:
    print(f"Error retrieving model info: {e}")
    raise

#sets up Hugging Face pipeline for text generation  
llama_pipe = pipeline("text-generation", model="daryl149/llama-2-7b-hf")

template = """
You are an assistant that helps people find information from a movie database.
Given a movie name, provide the genre of the movie.
Movie name: {movie_name}
Response: The genre of the movie "{movie_name}" is {genre}.
"""
prompt = PromptTemplate(template=template, input_variables=["movie_name", "genre"])

#formats it into a prompt using the PromptTemplate, runs the LLAMA-2 model pipeline
def llama_chain_run(input_data):
    prompt_text = prompt.format(**input_data)
    response = llama_pipe(prompt_text, max_length=50, num_return_sequences=1)[0]['generated_text']
    return response


def get_movie_info(movie_name):
    genre = get_movie_genre(movie_name)
    response = llama_chain_run({"movie_name": movie_name, "genre": genre})
    return response



if __name__ == "__main__":
    movie_name = "Titanic"
    response = get_movie_info(movie_name)
    print(response)
