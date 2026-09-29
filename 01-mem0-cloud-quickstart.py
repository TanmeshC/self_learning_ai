from mem0 import MemoryClient
from dotenv import load_dotenv
import os

load_dotenv(".env", override=True)

# --------------------------------------------------------------
# Initialize Mem0 client (Cloud)
# --------------------------------------------------------------

client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))

# --------------------------------------------------------------
# Message sequence
# --------------------------------------------------------------

messages = [
    {
        "role": "user",
        "content": "Hi, I'm User. I like to build AI automations!.",
    },
    {
        "role": "assistant",
        "content": "Hello User! I've noted that you like to build AI automations!. I'll keep this in mind for any AI automation related recommendations or discussions.",
    },
]

client.add(messages, user_id="default_user")

# --------------------------------------------------------------
# Search for related memories
# --------------------------------------------------------------

query = "What shall we build today?"
response = client.search(query, filters={"user_id": "default_user"})
print(response)
