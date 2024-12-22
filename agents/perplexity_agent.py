from phi.agent import Agent
from tools.perplexity_tools import PerplexitySearch
from phi.model.groq import Groq
from dotenv import load_dotenv
from phi.agent import Agent, RunResponse

from typing import Iterator

load_dotenv()
model = Groq(id="llama3-groq-70b-8192-tool-use-preview")

def get_perplexity_search(query: str) -> str:
    """
    Wrapper function to perform Perplexity search and get summarized results
    """
    perplexity_tool = PerplexitySearch(api_key="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")
    search_results = perplexity_tool.perplexity_search(query)
    
    agent = Agent(
        instructions=[
            "You are a summariser agent. Summarize the input you have.",
        ],
        tools=[],
        show_tool_calls=False,
        model=model,
        debug_mode=False,
    )
    #response: RunResponse = agent.print_response(search_results, markdown=True)

    response_text = ""
    response_iterator = agent.run(search_results, markdown=True, stream=True)
    for chunk in response_iterator:
        if isinstance(chunk, RunResponse):
            response_text += chunk.content
    return response_text

    
    
    #return response
