import requests
import os 
from dotenv import load_dotenv

load_dotenv()

ALPHAKEK_API_KEY = os.getenv("ALPHAKEK_API_KEY")

def alphakek_agent(model , query:str)->str:

    response = requests.post(
    "https://api.alphakek.ai/v1/chat/completions",
    headers={"Authorization":f"Bearer {ALPHAKEK_API_KEY}","Content-Type":"application/json"},
    json={"model":model,"messages":[{"role":"system","content":query}]})
    
    data = response.json()
    
    return data


#alphakek_agent("eclipse" ,"what is the value of sol")




#hey = alphakek_agent( "eclipse", "what is the curent value of solana ")
# content = hey['choices'][0]['message']['content']








