from textwrap import dedent
from datetime import datetime
from phi.agent import Agent
from model import model

class ProjectScorer:
    def __init__(self):
        self.agent = Agent(
            model=model,
            tools=[],
            description="You are an advanced AI analyst specializing in web3 project evaluation. You will analyze data and provide a comprehensive report with scoring.",
            instructions=[
                """
                You are provided with a dataset containing information about a project.
                This data includes details about the team, the technology, the market, and the tokenomics.
                Your task is to analyze this data and create a comprehensive report in markdown format that includes scoring calculations.
                remember to always score slowly and out of 100 """
            ],
            expected_output=dedent("""\
                ## Web3 Project Scoring Analysis

                ### Team Analysis Score:
                - Prior Web3 Success: [X] points
                - Technical Expertise: [X] points
                - Team Completeness: [X] points
                **Team Total: [X]/30**

                ### Technology Analysis Score:
                - Technical Differentiation: [X] points
                - Technical Feasibility: [X] points
                - Security & Architecture: [X] points
                **Technology Total: [X]/25**

                ### Market Analysis Score:
                - Market Size: [X] points
                - Competition & Positioning: [X] points
                - Go-to-Market Strategy: [X] points
                **Market Total: [X]/25**

                ### Token Analysis Score:
                - Token Utility: [X] points
                - Economic Design: [X] points
                - Distribution & Supply: [X] points
                **Token Total: [X]/20**

                ### Bonus & Penalty Points:
                Bonus Points (+[X]):
                [List bonus points awarded]

                Penalty Points (-[X]):
                [List penalty points deducted]

                ### Total Score Calculation:
                [Detailed score calculation]
                **Final Score: [X]/100**
                

                Published on {datetime.now().strftime("%d/%m/%Y")}
            """),
            markdown=True,
            show_tool_calls=True,
        )
        self.scoring_rubric = """
        ### Section 1: Team Analysis
        Score the team on a scale of 0 to 30 based on the following rubric:

        **Prior Web3 Success (10 points)**
        - 10: Founded successful Web3 project with proven track record
        - 7: Senior role in successful Web3 project
        - 4: Junior role in Web3 project
        - 0: No Web3 experience

        **Technical Expertise (10 points)**
        - 10: Strong technical team with Rust/Solana experience
        - 7: Strong technical team learning Solana
        - 4: Outsourced development with good oversight
        - 0: Limited technical capability

        **Team Completeness (10 points)**
        - 10: Full team covering tech, product, business, community
        - 7: Most key roles filled with clear hiring plan
        - 4: Core team only with gaps
        - 0: Significant gaps in team

        ### Section 2: Technology Analysis
        Score the technology on a scale of 0 to 25 using the following rubric:

        **Technical Differentiation (10 points)**
        - 10: Novel solution with clear technical moat
        - 7: Significant improvements to existing solutions
        - 4: Minor improvements to existing solutions
        - 0: No clear technical differentiation

        **Technical Feasibility (10 points)**
        - 10: Working prototype/MVP
        - 7: Technical specification and development progress
        - 4: Theoretical solution with clear development path
        - 0: Unclear technical feasibility

        **Security & Architecture (5 points)**
        - 5: Comprehensive security model with audits
        - 3: Clear security considerations and plans
        - 0: Limited security consideration

        ### Section 3: Market Analysis
        Score the market on a scale of 0 to 25 using the following rubric:

        **Market Size (10 points)**
        - 10: Large addressable market with clear growth
        - 7: Medium market with growth potential
        - 4: Niche market
        - 0: Unclear market size

        **Competition & Positioning (10 points)**
        - 10: Clear competitive advantage in growing market
        - 7: Competitive offering in established market
        - 4: Me-too product with slight differentiation
        - 0: Highly competitive market with no clear advantage

        **Go-to-Market Strategy (5 points)**
        - 5: Clear, realistic GTM with existing traction
        - 3: Defined GTM strategy
        - 0: Vague GTM plans

        ### Section 4: Token Analysis
        Score the token on a scale of 0 to 20 using the following rubric:

        **Token Utility (8 points)**
        - 8: Token is essential to protocol function
        - 5: Token adds clear value but isn't essential
        - 2: Limited token utility
        - 0: No clear token utility

        **Economic Design (8 points)**
        - 8: Well-designed economics with clear value capture
        - 5: Solid economics with some questions
        - 2: Basic economic model
        - 0: Problematic economic design

        **Distribution & Supply (4 points)**
        - 4: Fair distribution with proper vesting
        - 2: Standard distribution model
        - 0: Concerning distribution model

        ### Bonus & Penalty Points
        **Bonus Points** (+2 each, max +10)
        - Strong Network Effects: Clear evidence of increasing value with user growth
        - Capital Efficient Growth: Low burn rate with clear path to sustainability
        - Clear Revenue Model: Existing revenue or clear monetization strategy
        - Exclusive Deal Access: Unique partnerships or market access
        - Low Token Valuation: Attractive valuation compared to peers

        **Penalty Points** (-2 each, up to -10)
        - High Regulatory Risk: Clear regulatory concerns
        - Overcrowded Market: Too many well-funded competitors
        - Overly Complex Token Economics: Unnecessary complexity
        - Weak Value Capture: Unclear path to value accrual
        - Not Crypto Native Team: Limited crypto understanding
        - Team Fraud: Any history of fraudulent behavior
        do not be so rigid also give score for a good proposal based on what you decide from 10 to 20 points
        """

    def analyze_project(self, project_data):
        """
        Analyze a web3 project and return a detailed scoring breakdown.
        
        Args:
            project_data (dict): Dictionary containing project information
                               with the expected structure for team, github,
                               market, and token data.
        
        Returns:
            str: Markdown formatted analysis report
        """
        prompt = f"""Please analyze this web3 project data and provide a detailed scoring breakdown using the provided rubric:

        Project Data:
        {project_data}

        Scoring Rubric:
        {self.scoring_rubric}

        Please provide detailed point calculations and explanations for each category."""

        return self.agent.run(prompt)
    

#     to be used in the main.py File  
#     scorer = ProjectScorer()

# hello = scorer.analyze_project(technical_project)

# print(hello.content)
