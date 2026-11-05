
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import (
    TextMentionTermination,
    MaxMessageTermination
)

from agents.query_agent import query_agent
from agents.knowledge_agent_autogen import knowledge_agent
from agents.resolution_agent import resolution_agent
from agents.log_agent import log_agent


# Stop when the Log Agent finishes or the safety limit is reached.
termination = (
    TextMentionTermination("TICKET_REVIEW_COMPLETE")
    | MaxMessageTermination(8)
)


# Connect the four agents in the required sequence.
support_team = RoundRobinGroupChat(
    participants=[
        query_agent,
        knowledge_agent,
        resolution_agent,
        log_agent
    ],
    termination_condition=termination
)
