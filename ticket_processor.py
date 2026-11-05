
import re
import json

from team import support_team
from ticket_logger import save_ticket


def get_agent_text(messages, agent_name):
    """Get the final text response from a particular agent."""

    for message in reversed(messages):
        if (
            message.source == agent_name
            and isinstance(message.content, str)
            and message.content.strip()
        ):
            return message.content

    return ""


def parse_classification(query_result):
    """Extract classification fields from JSON or numbered text."""

    category = "Unknown"
    urgency = "Unknown"
    sentiment = "Unknown"

    clean_result = query_result.strip()

    # First, try to parse JSON.
    clean_result = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        clean_result,
        flags=re.IGNORECASE
    )

    try:
        classification = json.loads(clean_result)

        if isinstance(classification, dict):
            fields = {
                str(key).lower(): value
                for key, value in classification.items()
            }

            category = fields.get("category", category)
            urgency = fields.get("urgency", urgency)
            sentiment = fields.get("sentiment", sentiment)

            return (
                str(category).strip(),
                str(urgency).strip(),
                str(sentiment).strip()
            )

    except (json.JSONDecodeError, AttributeError):
        pass

    # If JSON parsing fails, extract numbered-text fields.
    def extract_field(field_name):
        pattern = (
            rf"^\s*(?:\d+[\.\)]\s*)?"
            rf"{re.escape(field_name)}\s*:\s*(.+?)\s*$"
        )

        match = re.search(
            pattern,
            query_result,
            re.IGNORECASE | re.MULTILINE
        )

        return match.group(1).strip() if match else "Unknown"

    category = extract_field("Category")
    urgency = extract_field("Urgency")
    sentiment = extract_field("Sentiment")

    return category, urgency, sentiment


async def process_ticket(customer_name, order_id, complaint):

    task = f"""
    Customer Name: {customer_name}
    Order ID: {order_id}

    Customer Complaint:
    {complaint}

    Follow your assigned responsibilities.
    Use retrieved company policy as the source of truth.
    Complete the ticket review.
    """

    result = await support_team.run(task=task)
    messages = result.messages

    # Collect each agent's final response.
    query_result = get_agent_text(
        messages, "customer_query_agent"
    )

    kb_result = get_agent_text(
        messages, "knowledge_base_agent"
    )

    resolution_result = get_agent_text(
        messages, "resolution_agent"
    )

    log_result = get_agent_text(
        messages, "log_agent"
    )

    # Extract classification from JSON or numbered text.
    category, urgency, sentiment = parse_classification(
        query_result
    )

    # Extract policy source filenames.
    sources = list(dict.fromkeys(
        re.findall(r"Source:\s*([A-Za-z0-9_.-]+)", kb_result)
    ))

    kb_sources = ", ".join(sources) if sources else "No match"

    # Extract customer response.
    response_match = re.search(
        r"Customer Response:\s*(.*?)\s*Confidence:",
        resolution_result,
        re.IGNORECASE | re.DOTALL
    )

    response = (
        response_match.group(1).strip()
        if response_match
        else resolution_result
    )

    # Extract and normalize confidence.
    confidence_match = re.search(
        r"Confidence:\s*\[?([A-Za-z]+)\]?",
        resolution_result,
        re.IGNORECASE
    )

    confidence = (
        confidence_match.group(1).capitalize()
        if confidence_match
        else "Unknown"
    )

    # Extract Log Agent status.
    status_match = re.search(
        r"Status:\s*(Resolved|Escalated)",
        log_result,
        re.IGNORECASE
    )

    status = (
        status_match.group(1).capitalize()
        if status_match
        else "Escalated"
    )

    # Extract Log Agent escalation reason.
    reason_match = re.search(
        r"Escalation_Reason:\s*(.*)",
        log_result,
        re.IGNORECASE
    )

    escalation_reason = (
        reason_match.group(1).strip()
        if reason_match
        else "Review required"
    )

    # ------------------------------------------------
    # DETERMINISTIC ESCALATION SAFEGUARDS
    # ------------------------------------------------

    mandatory_reasons = []

    # High urgency must always be escalated.
    if urgency.lower() == "high":
        mandatory_reasons.append("High urgency")

    # Angry customers must always be escalated.
    if sentiment.lower() == "angry":
        mandatory_reasons.append("Angry customer sentiment")

    # Low confidence must always be escalated.
    if confidence.lower() == "low":
        mandatory_reasons.append("Low resolution confidence")

    # Missing knowledge base match must be escalated.
    if (
        "NO_KB_MATCH" in kb_result
        or not sources
    ):
        mandatory_reasons.append(
            "No relevant knowledge base policy found"
        )

    # Preserve existing reasons from the Log Agent.
    if escalation_reason.lower() not in ["none", ""]:
        mandatory_reasons.append(escalation_reason)

    # Remove exact duplicate reasons.
    mandatory_reasons = list(dict.fromkeys(mandatory_reasons))

    # Apply the final status.
    if mandatory_reasons:
        status = "Escalated"
        escalation_reason = "; ".join(mandatory_reasons)

    elif status == "Escalated":
        escalation_reason = (
            "Manual review required"
            if escalation_reason.lower() in ["none", ""]
            else escalation_reason
        )

    else:
        escalation_reason = "None"

    # ------------------------------------------------
    # SAVE FINAL TICKET
    # ------------------------------------------------

    ticket_data = {
        "customer_name": customer_name,
        "order_id": order_id,
        "complaint": complaint,
        "category": category,
        "urgency": urgency,
        "sentiment": sentiment,
        "kb_sources": kb_sources,
        "response": response,
        "status": status,
        "escalation_reason": escalation_reason
    }

    ticket_id = save_ticket(ticket_data)

    # Reset the team before processing another ticket.
    await support_team.reset()

    return {
        "ticket_id": ticket_id,
        "category": category,
        "urgency": urgency,
        "sentiment": sentiment,
        "kb_sources": kb_sources,
        "response": response,
        "confidence": confidence,
        "status": status,
        "escalation_reason": escalation_reason
    }
