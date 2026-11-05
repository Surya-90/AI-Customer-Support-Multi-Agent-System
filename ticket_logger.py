
import csv
import uuid
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "tickets.csv"

COLUMNS = [
    "ticket_id",
    "timestamp",
    "customer_name",
    "order_id",
    "complaint",
    "category",
    "urgency",
    "sentiment",
    "kb_sources",
    "response",
    "status",
    "escalation_reason"
]


def save_ticket(ticket_data):

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    file_exists = LOG_FILE.exists()

    ticket_data["ticket_id"] = (
        "BN-" + uuid.uuid4().hex[:8].upper()
    )

    ticket_data["timestamp"] = (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    with open(
        LOG_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=COLUMNS
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(ticket_data)

    return ticket_data["ticket_id"]


def get_tickets():

    if not LOG_FILE.exists():
        return []

    with open(
        LOG_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        return list(csv.DictReader(file))
