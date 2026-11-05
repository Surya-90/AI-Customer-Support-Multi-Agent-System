
import asyncio
from agents.resolution_agent import resolution_agent


async def main():
    customer_complaint = (
        "I forgot my password and cannot log in."
    )

    classification = """
    Category: Account
    Urgency: Medium
    Sentiment: Frustrated
    """

    retrieved_policy = """
    Source: account_and_login.md

    Resetting Your Password:
    1. Go to the login page and click Forgot Password.
    2. Enter the email address on your account.
    3. Check your inbox for the reset email.
    4. The reset link expires in 30 minutes.
    5. If you don't see the email, check spam and wait
       5 minutes before requesting another.
    6. Maximum 3 reset emails per hour.
    """

    task = f"""
    Customer complaint:
    {customer_complaint}

    Classification:
    {classification}

    Retrieved company policy:
    {retrieved_policy}

    Write a customer-ready response using only this policy.
    """

    result = await resolution_agent.run(task=task)

    print("\nRESOLUTION AGENT RESULT:\n")
    print(result.messages[-1].content)


asyncio.run(main())
