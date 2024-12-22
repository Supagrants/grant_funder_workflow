#agent to create a dealmemo

from textwrap import dedent
from datetime import datetime
from phi.agent import Agent
from model import model

class DealMemoAgent:
    def __init__(self):
        self.agent = Agent(
            model=model,
            tools=[],
            description="You are an experienced investment analyst specializing in web3 projects. You create detailed deal memos that help inform investment decisions.",
            instructions=[
                """
                You will analyze project data and create a comprehensive deal memo that covers all critical aspects.
                Your analysis should be thorough yet concise, highlighting key strengths, risks, and opportunities.
                Structure your response in a clear, professional format that aids decision-making.
                """
            ],
            expected_output=dedent("""\
                # Investment Deal Memo
                **Project Name**: [Project Name]
                **Date**: {datetime.now().strftime("%d/%m/%Y")}
                **Analyst**: AI Investment Analyst

                ## Executive Summary
                [2-3 sentences on the project's core value proposition]

                ## Team Assessment
                - **Key Team Members**: [List key members and backgrounds]
                - **Track Record**: [Prior successes/experience]
                - **Gaps/Concerns**: [Any notable missing roles or concerns]

                ## Product & Technology
                - **Core Innovation**: [Key technological differentiators]
                - **Development Stage**: [Current state of product]
                - **Technical Architecture**: [Key technical components]
                - **Security Considerations**: [Security measures and risks]

                ## Market Opportunity
                - **Target Market**: [Size and characteristics]
                - **Competition**: [Key competitors and differentiators]
                - **Go-to-Market Strategy**: [Distribution and growth plans]

                ## Token Economics
                - **Token Utility**: [Core token use cases]
                - **Distribution**: [Token allocation and vesting]
                - **Value Capture**: [How value accrues to token]

                ## Investment Terms
                - **Valuation**: [Current valuation]
                - **Round Details**: [Investment structure]
                - **Key Terms**: [Important terms and conditions]

                ## Risk Assessment
                - **Technical Risks**: [Key technical challenges]
                - **Market Risks**: [Market-related concerns]
                - **Regulatory Risks**: [Compliance considerations]
                - **Team Risks**: [Team-related concerns]

                ## Investment Thesis
                [3-4 key reasons why this is/isn't a compelling investment]

                ## Recommendation
                [Clear investment recommendation with supporting rationale]
                """),
            markdown=True,
            show_tool_calls=True,
        )
  

    def deal_memo_agent(self, deal_memo_prompt):

        prompt = f"""Please analyze this web3 project and create a comprehensive deal memo that covers all key aspects of the investment opportunity:

        Project Information:
        {deal_memo_prompt}

        Please be thorough in your analysis, highlighting both opportunities and risks. Support your recommendations with clear rationale."""

        return self.agent.run(prompt).content
    

#     to be used in the main.py File  
#     scorer = ProjectScorer()

# hello = scorer.analyze_project(technical_project)

# print(hello.content)