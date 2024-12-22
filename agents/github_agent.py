from phi.agent import Agent
from phi.tools.github import GithubTools
import os
from datetime import datetime, timedelta
from phi.agent import Agent, RunResponse
from phi.utils.pprint import pprint_run_response
from model import model

# from phi.model.groq import Groq
# from phi.model.xai import xAI

# model=Groq(id="llama3-groq-70b-8192-tool-use-preview")

#from github_tools import GithubCommitStats, GithubPullRequestStats
from tools.github_tools import GithubCommitStats, GithubPullRequestStats
github_pull_request_stats = GithubPullRequestStats()
github_commit_stats = GithubCommitStats()


# Get Github token from environment variable, or use None if not set
github_token = os.getenv("GITHUB_ACCESS_TOKEN")


class GithubAnalyzer:
    def __init__(self, github_token=None):
        self.github_token = github_token or os.getenv("GITHUB_ACCESS_TOKEN")
        if not self.github_token:
            raise ValueError("GitHub token not found")

        self.github_pull_request_stats = GithubPullRequestStats()
        self.github_commit_stats = GithubCommitStats()
        self.model = model
        
        self.agent = Agent(
            instructions=[
                "Use your tools to analyze GitHub repositories",
                "Use GithubPullRequestStats() for finding pull requests",
                "Use GithubCommitStats() for finding commits",
            ],
            model=self.model,
            tools=[
                GithubTools(access_token=self.github_token),
                self.github_commit_stats,
                
            ],
            show_tool_calls=True,
        )

    def analyze_repository(self, repo_owner: str, repo_name: str):
        prompt = f"""Analyze the GitHub repository {repo_owner}/{repo_name}.
        Provide information about:
        - list Recent commits
        - list Pull requests
        - Development activity"""

        response: RunResponse = self.agent.run(prompt)
        #pprint_run_response(response, markdown=True)

        #response = self.agent.print_response(prompt, markdown=True , stream=True)
        return response.content

