from phi.agent import Agent
from model import model

from phi.agent import Agent, RunResponse
from phi.utils.pprint import pprint_run_response
from typing import Iterator


class SummaryAgent:
    def __init__(self):
        self.agent = Agent(
            model=model,
            instructions=[
                "You are a data extraction specialist for web3 projects.",
                "Your role is to analyze project documentation and extract specific data points needed by other agents.",
                "Structure the output carefully to ensure it can be used by specialized analysis agents.",
            ],
            structured_outputs=True,
        )

    def extract_project_data(self, text: str) -> str:
        prompt = f"""
        Analyze the following project information and extract key data points in a structured format:

        {text}

        Extract and organize the following information:
        1. Project name
        2. All GitHub repository references (in owner/repo format)
        3. Names of founders and key team members
        4. Any wallet addresses mentioned
        5. Grant amount requested (if mentioned)
        6. Technical stack and frameworks used
        7. Key market-related terms for research
        8. Blockchain networks involved
        """

        # Run the agent and get the response
        response_stream: Iterator[RunResponse] = self.agent.run(prompt, stream=False)

        # Access the content from the last message in the response
        content_output = response_stream.messages[-1].content
        print(content_output)

        return content_output

#summary agent for to find particular data for  agents 