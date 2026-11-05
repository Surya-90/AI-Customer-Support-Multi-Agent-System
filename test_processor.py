
import asyncio
from ticket_processor import process_ticket


async def main():

    result = await process_ticket(
        customer_name="Sarah Johnson",
        order_id="BN-ORD-2001",
        complaint=(
            "I received my order 10 days ago and want to return an unused item."
            
        )
    )

    print("\n========== FINAL TICKET RESULT ==========\n")

    for key, value in result.items():
        print(f"{key}: {value}")


asyncio.run(main())
