
import asyncio
from agents.log_agent import log_agent


async def main():
    task = """
    Customer Complaint:
    My payment was deducted twice for the same order.
    I want my money back immediately.

    Classification:
    Category: Other
    Urgency: High
    Sentiment: Angry

    Knowledge Base:
    No relevant payment dispute policy was found.

    Resolution:
    Confidence: Low
    Escalation Required: Yes
    """

    result = await log_agent.run(task=task)

    print("\nLOG AGENT RESULT:\n")
    print(result.messages[-1].content)


asyncio.run(main())
