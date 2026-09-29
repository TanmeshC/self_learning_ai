import os

from dotenv import load_dotenv
from mem0 import Memory

load_dotenv(".env", override=True)

# --------------------------------------------------------------
# Ollama config (replaces the OpenAI default)
# --------------------------------------------------------------
# Pull the models first: `ollama pull llama3.1` and `ollama pull nomic-embed-text`
#
# .env should have (only OLLAMA_API_KEY is needed if you're using Ollama Cloud
# or a remote host that requires auth — a local install needs no key at all):
#   OLLAMA_BASE_URL=http://localhost:11434
#   OLLAMA_API_KEY=your_ollama_key   # optional, remote/cloud only

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")  # optional

if OLLAMA_API_KEY:
    # mem0's ollama client reads this env var for authenticated hosts
    os.environ["OLLAMA_API_KEY"] = OLLAMA_API_KEY

config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1:latest",
            "temperature": 0.1,
            "max_tokens": 2000,
            "ollama_base_url": OLLAMA_BASE_URL,
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            "ollama_base_url": OLLAMA_BASE_URL,
        },
    },
}

m = Memory.from_config(config)  # Uses Ollama for both LLM + embeddings (in-process, not long-term)

# --------------------------------------------------------------
# Message sequence
# --------------------------------------------------------------

messages = [
    {
        "role": "user",
        "content": "I'm planning to watch a movie tonight. Any recommendations?",
    },
    {
        "role": "assistant",
        "content": "How about a thriller movies? They can be quite engaging.",
    },
    {
        "role": "user",
        "content": "I'm not a big fan of thriller movies but I love sci-fi movies.",
    },
    {
        "role": "assistant",
        "content": "Got it! I'll avoid thriller recommendations and suggest sci-fi movies in the future.",
    },
]

# --------------------------------------------------------------
# Store inferred memories (default behavior)
# --------------------------------------------------------------

result = m.add(
    messages, user_id="default_user", metadata={"category": "movie_recommendations"}
)
print("Add result:", result)

# --------------------------------------------------------------
# Get all memories
# --------------------------------------------------------------

all_memories = m.get_all(filters={"user_id": "default_user"})
print("All memories:", all_memories)

# --------------------------------------------------------------
# Search for related memories
# --------------------------------------------------------------

related_memories = m.search(
    query="What do you know about me?", filters={"user_id": "default_user"}
)
print(related_memories)
