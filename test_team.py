
import asyncio
from team import support_team


async def main():

    customer_complaint = """
    I am extremely angry. My NestCam arrived broken, and nobody is helping me. I want this resolved immediately.
    """

    print("\nSTARTING BRIGHTNEST CUSTOMER SUPPORT TEAM...\n")

    result = await support_team.run(
        task=customer_complaint
    )

    print("\n========== AGENT WORKFLOW ==========\n")

    for message in result.messages:
        print(f"\nAGENT: {message.source}")
        print("-" * 50)
        print(message.content)

    print("\n========== WORKFLOW COMPLETED ==========\n")


asyncio.run(main())
