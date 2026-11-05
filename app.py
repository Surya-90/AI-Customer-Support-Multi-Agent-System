
import asyncio

import pandas as pd
import streamlit as st

from ticket_processor import process_ticket
from ticket_logger import get_tickets


# Reuse one event loop across Streamlit reruns.
@st.cache_resource
def get_event_loop():
    return asyncio.new_event_loop()


# Page configuration
st.set_page_config(
    page_title="BrightNest Customer Support",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 BrightNest Home")
st.subheader("AI Customer Support Desk")

st.write(
    "Submit a customer complaint and let our four AI agents "
    "classify, investigate, draft a response, and review the ticket."
)

st.divider()


# Customer complaint form
st.header("Submit a Customer Complaint")

with st.form("customer_support_form"):

    customer_name = st.text_input("Customer Name")

    order_id = st.text_input("Order ID")

    complaint = st.text_area(
        "Customer Complaint",
        height=150,
        placeholder="Describe the customer's issue..."
    )

    submitted = st.form_submit_button(
        "Process Customer Ticket",
        type="primary"
    )


# Process customer ticket
if submitted:

    if not customer_name.strip() or not complaint.strip():

        st.error("Customer Name and Complaint are required.")

    else:

        try:
            with st.spinner(
                "Our AI agents are reviewing the customer complaint..."
            ):

                loop = get_event_loop()

                result = loop.run_until_complete(
                    process_ticket(
                        customer_name.strip(),
                        order_id.strip(),
                        complaint.strip()
                    )
                )

            st.session_state["ticket_result"] = result

            st.success("Ticket processing completed!")

        except Exception as error:
            st.error(f"Ticket processing failed: {error}")


# Display latest ticket result
if "ticket_result" in st.session_state:

    result = st.session_state["ticket_result"]

    st.divider()
    st.header("Ticket Processing Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Category", result["category"])

    with col2:
        st.metric("Urgency", result["urgency"])

    with col3:
        st.metric("Sentiment", result["sentiment"])

    st.write(f"**Ticket ID:** {result['ticket_id']}")

    st.write(f"**Knowledge Base Sources:** {result['kb_sources']}")

    st.write(f"**Confidence:** {result['confidence']}")

    if result["status"] == "Resolved":

        st.success("Status: Resolved")

    else:

        st.error("Status: Escalated")

        st.warning(
            f"Escalation Reason: {result['escalation_reason']}"
        )

    st.subheader("Customer Response")

    st.text_area(
        "Generated Response",
        value=result["response"],
        height=250
    )


# Ticket history
st.divider()
st.header("Ticket History")

tickets = get_tickets()

if tickets:

    tickets_df = pd.DataFrame(tickets)

    st.dataframe(
        tickets_df,
        width="stretch",
        hide_index=True
    )

    csv_data = tickets_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Ticket Logs (CSV)",
        data=csv_data,
        file_name="brightnest_ticket_logs.csv",
        mime="text/csv"
    )

else:

    st.info("No tickets have been logged yet.")
