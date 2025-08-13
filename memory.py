from agno.agent import Agent
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage
from agno.models.openai import OpenAIChat
import os
from dotenv import load_dotenv
from requests import session
from rich.pretty import pprint

# Load your environment variables from .env
load_dotenv()

# ✅ Make sure this is set in your .env file:
# OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_KEY:
    raise ValueError("⚠️ Please set OPENROUTER_API_KEY in your .env file.")

# SQLite database for sessions & memories
db_file = "tmp/agent_storage.db"
user_id = "Nitesh"

# Memory store
memory = Memory(
    db=SqliteMemoryDb(table_name="user_memories", db_file=db_file),
)

# Create the agent with OpenRouter Mistral model
agent = Agent(
    model=OpenAIChat(
        id="mistralai/mistral-7b-instruct",
        api_key=OPENROUTER_KEY,                   # ✅ Pass the key directly
        base_url="https://openrouter.ai/api/v1",  # ✅ Use OpenRouter API endpoint
    ),
    description="You’re an AI with a memory!",
    memory=memory,
    storage=SqliteStorage(table_name="agent_sessions", db_file=db_file),
    enable_user_memories=True,      # ✅ Enable fact extraction
    add_history_to_messages=True,   # Keeps conversation context
    num_history_runs=3,
    session_id="my_chat_session",
    markdown=True,
)

# Chat loop
while True:
    user_input = input("\nYou: ").strip()

    # Exit condition
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Goodbye! 👋")
        break

    # Agent response
    agent.print_response(user_input, user_id=user_id)

    # Show stored memories
    print("\nCurrent **memories** about the user:")
    user_memories = memory.get_user_memories(user_id=user_id)
    if not user_memories:
        print("No memories yet.")
    else:
        for i, m in enumerate(user_memories, start=1):
            topics = ", ".join(m.topics) if m.topics else "None"
            print(f"{i}. Memory: {m.memory} | Topics: {topics}")

# Get all sessions (if you don't know the session_id)
# all_sessions = agent.storage.get_all_sessions(user_id=user_id)
# for session in all_sessions:
#     # Attribute access for AgentSession object
#     user_id = session.user_id

#     # Key access for dictionary memory
#     for i in range(len(session.memory["runs"])):
#         conversation = session.memory["runs"][i]["content"]



#         print("User ID:", user_id)
#         print("Conversation:", conversation)


# Get messages from a specific session (like "my_chat_session")
