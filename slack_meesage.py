import slack
import os
from dotenv import load_dotenv

load_dotenv()

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


def send_markdown_message(channel, markdown_text):
  client.chat_postMessage(
            channel=channel,
            text=markdown_text,
        )
