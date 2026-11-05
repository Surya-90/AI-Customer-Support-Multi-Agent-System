
import asyncio
from agents.knowledge_agent_autogen import knowledge_agent


async def main():
    result = await knowledge_agent.run(
        task="""
        A customer says:
        'I forgot my password and cannot log in.'

        Find the relevant BrightNest Home policy.
        Use your search tool.
        Return the relevant instructions and source filename.
        Do not invent any information.
        """
    )

    print("\nKNOWLEDGE BASE AGENT RESULT:\n")

    for message in result.messages:
        print(f"\n{message.source}:")
        print(message.content)


asyncio.run(main())
