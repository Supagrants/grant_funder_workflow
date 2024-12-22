from langchain_core.prompts import ChatPromptTemplate
from typing import Optional, List, Dict
from typing_extensions import Annotated, TypedDict
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


import os
from dotenv import load_dotenv
load_dotenv()


# Define the TypedDict for your project data
class TeamMember(TypedDict):
    name: str
    role: str
    email: Optional[str]
    discord_handle: Optional[str]
    twitter_handle: Optional[str]



class ProjectData(TypedDict):
    project_name: str
    github_repositories: List[str]
    team_members: List[TeamMember]
    wallet_addresses: List[Dict[str, str]]
    grant_amount_requested: int
    technical_stack: List[str]
    market_keywords: List[str]
    blockchain_networks: List[str]


def process_project_data(project_data: ProjectData):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=None,
                                timeout=None,
                                max_retries=2,
                                )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that takes the input, which is formatted in a json-like format, and returns it as a valid, parseable JSON string. Do not change the structure of the data or the data itself, only make sure the formatting is correct and can be loaded as json. Include all top-level fields of the original json in the output. Do not include any explanations in your response, just output the json string"
            ),
            ("human", "Convert the following to valid json. Do not change the data, or the structure, only ensure it can be parsed as a json object: {input}"),
        ]
    )
    parser = JsonOutputParser(pydantic_schema=ProjectData)
    chain = prompt | llm | parser

    try:
        ai_msg = chain.invoke({"input": project_data})
        data = ai_msg

        project_name = data.get('project_name')
        github_repos = data.get('github_repositories', [])
        team_members = data.get('team_members', [])
        wallet_addresses = data.get('wallet_addresses', [])
        grant_amount = data.get('grant_amount_requested')
        technical_stack = data.get('technical_stack', [])
        market_terms = data.get('market_keywords', [])
        blockchain_networks = data.get('blockchain_networks', [])


        repo_owners = []
        repos = []

        # Make sure we are not iterating through an empty list and change them into empty strings if they are null
        if github_repos and isinstance(github_repos, list):
          for repo_str in github_repos:
                if "/" in repo_str:
                    owner, repo = repo_str.split("/")
                    repo_owners.append(owner)
                    repos.append(repo)
                else:
                    repo_owners.append(repo_str)
                    repos.append(repo_str)
        else:
             github_repos = "empty"


        founders = [member for member in team_members if member.get('role') in ['CEO', 'CTO', 'Founder']] if team_members else "empty"

        if not wallet_addresses:
             wallet_addresses = "empty"

        if not technical_stack:
            technical_stack = "empty"
        if not market_terms:
            market_terms = "empty"
        if not blockchain_networks:
             blockchain_networks = "empty"

        return {
            "project_name": project_name,
            "github_repos": github_repos,
            "team_members": team_members if team_members else "empty",
            "wallet_addresses": wallet_addresses,
            "grant_amount": grant_amount,
            "technical_stack": technical_stack,
            "market_terms": market_terms,
            "blockchain_networks": blockchain_networks,
            "repo_owners": repo_owners,
            "repos": repos,
            "founders": founders
         }
    except Exception as e:
        print(f"An error occurred during data processing: {e}")
        return None