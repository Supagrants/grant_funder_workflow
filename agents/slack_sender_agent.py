import os

from phi.agent import Agent
from phi.tools.slack import SlackTools

from model import model 

slack_token = os.getenv("SLACK_TOKEN")
if not slack_token:
    raise ValueError("SLACK_TOKEN not set")
slack_tools = SlackTools()

slack_sender_agent = Agent(tools=[slack_tools], 
              show_tool_calls=True , 
              model=model)

