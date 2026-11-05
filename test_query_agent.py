
import asyncio
from agents.query_agent import query_agent

async def main():
    result = await query_agent.run(
        task="My order has not arrived even though tracking says it was shipped 12 days ago. I am very frustrated."
    )

    print("\nCUSTOMER QUERY AGENT RESULT:\n")
    print(result.messages[-1].content)

asyncio.run(main())
