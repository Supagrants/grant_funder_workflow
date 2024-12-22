#dont need it 
# 
# #to generate a summary of the github agent response 

#takes the input of various run of the github agent and generates a summary of the response 

# the pull requests 
# agent.print_response("List monthly pull requests ", markdown=True , stream=True)


# Example 4: Get Pull Request activity
# print("\nPull request activity in the last month:\n")
# agent.print_response(f"List the pull requests in the last month since {formatted_start_date} and until {formatted_end_date}?",
#      markdown=True,
#      stream=True
# )

# print("\nIssue activity in the last month:\n")
# agent.print_response(f"List the issue events in the last month since {formatted_start_date} and until {formatted_end_date}?",
#      markdown=True,
#      stream=True
# )

from model import model
from phi.agent import Agent
github_summary_agent = Agent(
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    instructions=[
        "You are a text summarization expert.",
        "You will summarize a provided text, extracting the key information and insights.",
        "Be concise and clear in your summarization.",
    ],
    model = model,
    structured_outputs=True,
    show_tool_calls=True,
    debug_mode=True,
)
