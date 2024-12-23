from flask import Flask, request
from agents.github_agent import GithubAnalyzer
from agents.perplexity_agent import get_perplexity_search
from agents.scorer_agent import ProjectScorer
from agents.dealmemo_agent import DealMemoAgent
from agents.transaction_details_agent import TransactionDetailsAgent
from agents.summary_agent import SummaryAgent
from agents.helper_agent import process_project_data
from slack_meesage import send_markdown_message
from wallet import create_solana_transaction
from helper import combine_data_for_scoring, format_deal_memo_input

import json
from typing import Optional, Iterator
from pydantic import BaseModel, Field
from phi.agent import Agent
from phi.workflow import Workflow, RunResponse, RunEvent
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from phi.utils.pprint import pprint_run_response
from phi.utils.log import logger
from helper import combine_data_for_scoring, format_deal_memo_input


# importing agents
from agents.github_agent import GithubAnalyzer
from agents.perplexity_agent import get_perplexity_search

from agents.scorer_agent import ProjectScorer
from agents.slack_sender_agent import slack_sender_agent
from agents.alphakek_agent import alphakek_agent
from agents.dealmemo_agent import DealMemoAgent
from agents.transaction_details_agent import TransactionDetailsAgent
from agents.summary_agent import SummaryAgent
from agents.helper_agent import process_project_data
from slack_meesage import send_markdown_message
from wallet import create_solana_transaction

# importing model
from model import model


app = Flask(__name__)

# Initialize agents
scorer = ProjectScorer()
analyzer = GithubAnalyzer()
deal_memo_agent = DealMemoAgent()
transaction_agent = TransactionDetailsAgent()
summary_agent = SummaryAgent()

@app.route('/run', methods=['POST'])
def run_script():
    # Check for the text file in the request
    file = request.files.get('file')
    if not file or not file.filename.endswith('.txt'):
        return "Please upload a valid .txt file.", 400

    try:
        # Read the file content (assuming the uploaded file is a .txt file)
        text_content = file.read().decode('utf-8')  # Read and decode the file content
        # print(f"File content:\n{text_content}\n")  # Print file content for debugging

        # Original code starts here
        project_data = summary_agent.extract_project_data(text_content)
        # print(f"Project data extracted:\n{project_data}\n")  # Print extracted project data

        processed_data = process_project_data(project_data)
        # print(f"Processed data:\n{processed_data}\n")  # Print processed data

        repo_owner = processed_data['repo_owners']
        repo = processed_data['repos']
        github_response = analyzer.analyze_repository(repo_owner, repo)
        # print(f"GitHub analysis response:\n{github_response}\n")  # Print GitHub analysis response

        founder_details = f"Founders: {[founder['name'] for founder in processed_data['founders']]}"
        perplexity_query = (
            f"Provide detailed information about {founder_details}. "
            "Include their background, education, professional journey, notable achievements, "
            "and current ventures. If applicable, include links to their official websites, social media profiles, "
            "and recent interviews or publications."
        )
        # print(f"Perplexity query:\n{perplexity_query}\n")  # Print perplexity query
        perplexity_response = get_perplexity_search(perplexity_query)
        # print(f"Perplexity response:\n{perplexity_response}\n")  # Print perplexity response

        # Debugging alphakek input and output

        # Prepare the query for alphakek
        # Extract market_terms from processed_data
        alphakek_data = processed_data.get('market_terms', '')

        # Check if market_terms is empty or contains a placeholder like 'empty'
        if alphakek_data == 'empty' or not alphakek_data:
            # print("Warning: market_terms is empty or contains 'empty'. Using default value.")
            alphakek_data = "general market trends"  # You can set a fallback value here

        # Prepare the alphakek query
        alphakek_query = f"Check the market analysis of {processed_data['project_name']} from the point of view of {alphakek_data}"

        # Print the query to verify it's correct
        # print(f"alphakek query: {alphakek_query}")

        # Too slow 
        # alphakek_response = alphakek_agent("eclipse", alphakek_query)

        # Continue with the alphakek agent call
        alphakek_response = get_perplexity_search(alphakek_query)

        combined_analysis = combine_data_for_scoring(github_response, perplexity_response, alphakek_response)
        print(f"Combined analysis:\n{combined_analysis}\n")  # Print combined analysis

        scorer_response = scorer.analyze_project(combined_analysis)
        print(f"Scorer response:\n{scorer_response}\n")  # Print scorer response

        deal_memo_prompt = format_deal_memo_input(scorer_response, combined_analysis)
        print(f"Deal memo prompt:\n{deal_memo_prompt}\n")  # Print deal memo prompt
        deal_memo_response = deal_memo_agent.deal_memo_agent(deal_memo_prompt)
        print(f"Deal memo response:\n{deal_memo_response}\n")  # Print deal memo response

        budget = request.form.get("budget", "1000")
        print(f"Budget: {budget}")  # Print budget for debugging
        transaction_detail_response = transaction_agent.determine_transaction_details(
            grant_application=text_content, budget=budget, score=scorer_response)
        print(f"Transaction details response:\n{transaction_detail_response}\n")  # Print transaction details response

        sender_address_str = "C45KHyo1T5aSA4F4pXtMUhuhGbxTTHFaZyGXVzU7SHVp"
        recipient_address_str = "2cfbCMY2PXk4CB7J18abEPTR34TL2sGsjrMGmMyVVMWH"
        amount_to_transfer = 1

        if amount_to_transfer > 0:
            transaction_str = create_solana_transaction(sender_address_str, recipient_address_str, amount_to_transfer)
        else:
            transaction_str = "Amount must be greater than 0. Transaction not created."
        print(f"Transaction string:\n{transaction_str}\n")  # Print transaction string

        # Send messages to Slack
        channel = request.form.get("channel", "ai")
        print(f"Sending to channel: {channel}")  # Print the channel
        send_markdown_message(channel, deal_memo_response)
        send_markdown_message(channel, transaction_detail_response)
        send_markdown_message(channel, transaction_str)

        # Original code ends here
        return "Script executed successfully. Check Slack for details.", 200

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)

