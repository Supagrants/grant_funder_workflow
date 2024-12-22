import json
from typing import Optional, Iterator
from pydantic import BaseModel, Field
from phi.agent import Agent
from phi.workflow import Workflow, RunResponse, RunEvent
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from phi.utils.pprint import pprint_run_response
from phi.utils.log import logger
from helper import combine_data_for_scoring , format_deal_memo_input


#importing agents
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

#importing model
from model import model


#initalising
scorer = ProjectScorer()
analyzer = GithubAnalyzer()
deal_memo_agent = DealMemoAgent()
transaction_agent = TransactionDetailsAgent()
summary_agent = SummaryAgent()







if __name__ == "__main__":


    #getting file as a input 
    from rich.prompt import Prompt
    
    text_file_path = Prompt.ask("[bold]Enter path of text file[/bold]")
    #logger.info(f"Summarizing text file: {text_file_path}")

    #saving the file
    
    with open(text_file_path, "r") as file:
        text_content = file.read()


    #genrating summary/input for other agents

    project_data = summary_agent.extract_project_data(text_content)


    # feeding the project_data to different agents 


    # gettiing json from helper_agent 
    processed_data = process_project_data(project_data)




    #github agent 

    # getting repo from gerealagent for repo 

    repo_owner =f"{processed_data['repo_owners']}"
    repo=f"{processed_data['repos']}"
    
    github_response= analyzer.analyze_repository(repo_owner, repo)



    #perplexity agent 

    founder_details = f"Founders:{[founder['name'] for founder in processed_data['founders']]}"

    perplexity_query = (
        f"Provide detailed information about {founder_details}. "
        "Include their background, education, professional journey, notable achievements, "
        "and current ventures. If applicable, include links to their official websites, social media profiles, "
        "and recent interviews or publications."
    )




    perplexity_response = get_perplexity_search(perplexity_query)


    #alphakek agents 

    alphakek_data = f"All Data: {json.dumps(processed_data, indent=2)}"

    alphakek_query =" check the onchain activities of altriem ai "

    alphakek_response = alphakek_agent( "eclipse", alphakek_query)
    alphakek_response = alphakek_response['choices'][0]['message']['content']


    #scorer agent 

    combined_analysis = combine_data_for_scoring(github_response,perplexity_response, alphakek_response)


    scorer_response = scorer.analyze_project(combined_analysis)


    #deal memo agent 

    deal_memo_prompt = format_deal_memo_input(scorer_response, combined_analysis)


    deal_memo_response = deal_memo_agent.deal_memo_agent(deal_memo_prompt)


    #transaction detail agent 

    

    final_score = scorer_response

    #specify the budget 

    budget="1000"

    
    transaction_detail_response = transaction_agent.determine_transaction_details(grant_application=text_content, budget=budget, score=final_score)


    





    # sending slack messages 
    
    channel = "ai"

    #sendig deal memo 

    


    #deal_memo_message = f"Send a message '{deal_memo_response}' to the channel #ai"

    #slack_sender_agent.print_response( deal_memo_message, markdown=True)

    send_markdown_message(channel, deal_memo_response)






    # sending transaction detail 

    #transaction_detail_message = f"Send a message '{transaction_detail_response}' to the channel #ai"

    #slack_sender_agent.print_response( transaction_detail_message, markdown=True)

    send_markdown_message(channel, transaction_detail_response)


    # agent decides to wheter or not have a transaction 







    #intiating tranaction using crossmint wallet 







    # get amount to transfer from transaction_detail_response  

    # get the recipient adress from processed_data



    sender_address_str = "C45KHyo1T5aSA4F4pXtMUhuhGbxTTHFaZyGXVzU7SHVp"
    recipient_address_str = "2cfbCMY2PXk4CB7J18abEPTR34TL2sGsjrMGmMyVVMWH"
    amount_to_transfer = 1 
    

    # Check if the amount is greater than 
    
    if amount_to_transfer > 0:
        print("Amount is greater than 0. Proceeding with the transaction.")
        transaction_str = create_solana_transaction(sender_address_str, recipient_address_str, amount_to_transfer)
        # Further code to process the transaction
    else:
        print("Amount must be greater than 0. Transaction not created.")
        # Handle the invalid transaction scenario

    
    send_markdown_message(channel, transaction_str)
0






    #sending that trasaction is done through 
    
    
    # #add the wallet transaction code 

       

    

     




