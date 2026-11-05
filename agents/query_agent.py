
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

query_agent = AssistantAgent(
    name="customer_query_agent",
    model_client=model_client,
    system_message="""
You are a customer support query classification agent.

Your task is to analyze the customer's complaint.

Return these five fields:
1. Category: Shipping, Refund, Account, Product, or Other.
2. Urgency: Low, Medium, or High.
3. Sentiment: Positive, Neutral, Frustrated, or Angry.
4. Summary: A short summary of the complaint.
5. Escalation_Flag: Yes or No.

Rules:
- Use only information present in the customer complaint.
- Do not invent customer details.
- Set High urgency for serious complaints, legal threats,
  fraud, or payment disputes.
- Return the result in a clear, structured format.
"""
)
