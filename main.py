# !pip install -U agno
# !pip install python-dotenv

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os
from agno.agent import Agent

load_dotenv()
from agno.models.openai import OpenAIChat

# agno_agent = Agent(
#     model=OpenAIChat(
#         id="mistralai/mistral-7b-instruct",  # Or any OpenRouter model
#         api_key=os.getenv("OPENROUTER_API_KEY"),
#         base_url="https://openrouter.ai/api/v1"
#     ),
#     description="Agno Q&A agent",
#     markdown=False
# )



# file: simple_tool_example.py
from agno.agent import Agent
from agno.models.openai import OpenAIChat   # or any supported model
from agno.tools import tool
import random

@tool(show_result=True, stop_after_tool_call=True)
def get_weather(city: str) -> str:
    """Return a quick (fake/demo) weather report for `city`."""
    conditions = ["sunny", "cloudy", "rainy", "windy", "foggy"]
    temp = random.randint(15, 35)
    return f"Weather in {city}: {random.choice(conditions)}, {temp}°C"

agent = Agent(
   model=OpenAIChat(
        id="mistralai/mistral-7b-instruct",  # Or any OpenRouter model
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    ),
    tools=[get_weather],
    markdown=True,
)

agent.print_response("What's the weather in Mumbai today?", stream=True)
