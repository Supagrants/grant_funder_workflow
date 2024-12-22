from phi.agent import Agent
from phi.agent import Agent, RunResponse
from phi.utils.pprint import pprint_run_response
from typing import Iterator
from datetime import datetime
from textwrap import dedent
from model import model
class TransactionDetailsAgent:
    def __init__(self):
        self.agent = Agent(
            model=model,
            tools=[],
            description="You are a financial operations specialist who determines appropriate transaction details for web3 project grants.",
            instructions=[
                """
                You will analyze:
                1. The project's grant application
                2. Available budget
                3. Project score
                
                And determine:
                1. Whether to proceed with funding
                2. Appropriate funding amount within budget
                3. Verify wallet addresses
                
                Provide all details in a clear, structured format.
                Only proceed with funding recommendations for scores above 90.
                Validate that all wallet addresses are valid Solana addresses (base58, 32-44 characters).
                """
            ],
  
            markdown=True,
            show_tool_calls=False,
        )

    def determine_transaction_details(self, grant_application, budget, score):
        prompt = f"""
        Please analyze the following information and determine appropriate transaction details:

        Available Budget (SOL): {budget}
        Project Score: {score}
        
        Grant Application:
        {grant_application}

        Requirements:
        1. Only approve if score > 40.
        2. Score-based funding allocation:
            - Score 90-100: Full funding up to available budget.
            - Score 80-90: 80% of available budget.
            - Score 70-80: 60% of available budget.
            - Score 60-70: 40% of available budget.
            - Score 50-60: 20% of available budget.
            - Score 40-50: 10% of available budget.
        3. Funding amount must be within available budget.
        4. Verify all wallet addresses are valid Solana addresses.
        5. Provide clear rationale for funding decision and amount.
        
        Please provide complete transaction details following the expected format.
        """

        response_stream: Iterator[RunResponse] = self.agent.run(prompt , stream =False)

        content_output = response_stream.messages[-1].content

        return content_output
