
from autogen_agentchat.agents import AssistantAgent
from agents.query_agent import model_client
from agents.knowledge_agent import search_kb


def search_company_policies(query: str) -> str:
    """Search BrightNest Home policy documents."""

    results = search_kb(query, top_k=5)

    if not results:
        return "NO_KB_MATCH: No relevant company policy was found."

    output = []

    for result in results:
        output.append(
            f"Source: {result['source']}\n"
            f"Relevance Score: {result['score']}\n"
            f"Matched Words: {result['matched_words']}\n"
            f"Relevant Policy:\n{result['passage']}"
        )

    return "\n\n".join(output)


knowledge_agent = AssistantAgent(
    name="knowledge_base_agent",
    model_client=model_client,
    system_message="""
You are the BrightNest Home Knowledge Base Agent.

Your responsibility is to retrieve the most relevant company policies
for the customer's actual complaint.

IMPORTANT SEARCH INSTRUCTIONS:

1. Read the complete customer complaint carefully.
2. Identify the exact product, problem, and requested resolution.
3. Search using the customer's actual problem, not a vague category.
4. Include relevant alternative terms when searching.

Examples:

- Broken, faulty, defective, or damaged product:
  Search for the product name together with broken, defective,
  damaged, replacement, and refund.

- Delayed or missing package:
  Search for delayed delivery, missing package, shipment,
  tracking, and lost package.

- Forgotten password or login problem:
  Search for forgot password, login, reset password,
  and account lockout.

- Refund or return request:
  Search for refund, return, defective item,
  return shipping, and exchange.

5. You may perform more than one search when necessary.
6. Review the returned passages and identify the most relevant
   policies for the customer's specific problem.
7. Do not select a passage merely because it mentions the product.
8. Include the exact relevant policy conditions, time limits,
   fees, and exceptions when available.
9. Never invent company policies or promise unsupported outcomes.
10. If no relevant policy is found, clearly state that.
11. Always mention the source filename.
12. Do not write a customer response.

Use only the information returned by the search tool.
""",
    tools=[search_company_policies]
)
