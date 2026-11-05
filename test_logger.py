
from ticket_logger import save_ticket, get_tickets

ticket = {
    "customer_name": "John Smith",
    "order_id": "BN-ORD-1001",
    "complaint": "I forgot my password and cannot log in.",
    "category": "Account",
    "urgency": "Medium",
    "sentiment": "Frustrated",
    "kb_sources": "account_and_login.md",
    "response": "Please use the Forgot Password option.",
    "status": "Resolved",
    "escalation_reason": "None"
}

ticket_id = save_ticket(ticket)

print("Ticket saved successfully!")
print("Ticket ID:", ticket_id)

print("\nSAVED TICKETS:\n")

for saved_ticket in get_tickets():
    print(saved_ticket)
