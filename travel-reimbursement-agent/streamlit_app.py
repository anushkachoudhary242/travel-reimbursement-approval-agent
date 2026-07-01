import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/evaluate"

st.set_page_config(
    page_title="Travel Reimbursement Agent",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Travel Reimbursement Approval Agent")

st.markdown("---")

##########################################
# Employee Details
##########################################

st.header("Employee Details")

col1, col2 = st.columns(2)

with col1:

    employee_id = st.text_input(
        "Employee ID",
        "EMP001"
    )

    employee_name = st.text_input(
        "Employee Name",
        "Rahul Sharma"
    )

with col2:

    trip_location = st.text_input(
        "Trip Location",
        "Mumbai"
    )

##########################################
# Expenses
##########################################

st.header("Expense Details")

col1, col2 = st.columns(2)

with col1:

    hotel = st.number_input(
        "Hotel Expense",
        min_value=0.0,
        value=6000.0
    )

    meal = st.number_input(
        "Meal Expense",
        min_value=0.0,
        value=900.0
    )

    taxi = st.number_input(
        "Taxi Expense",
        min_value=0.0,
        value=800.0
    )

with col2:

    flight = st.selectbox(

        "Flight Class",

        [

            "Economy",

            "Business"

        ]

    )

    flight_amount = st.number_input(

        "Flight Fare",

        min_value=0.0,

        value=12000.0

    )

    shopping = st.number_input(

        "Shopping Expense",

        min_value=0.0,

        value=0.0

    )

##########################################
# Receipts
##########################################

st.header("Receipts")

receipt_options = [

    "receipt_001",

    "receipt_002",

    "receipt_003",

    "receipt_004",

    "receipt_005",

    "receipt_006",

    "receipt_007",

    "receipt_008",

    "receipt_009"

]

receipts = st.multiselect(

    "Select Uploaded Receipts",

    receipt_options,

    default=[]

)

##########################################
# Submit
##########################################

if st.button("Evaluate Claim"):

    payload = {

        "employee_id": employee_id,

        "employee_name": employee_name,

        "trip_location": trip_location,

        "hotel": hotel,

        "meal": meal,

        "taxi": taxi,

        "flight": flight,

        "flight_amount": flight_amount,

        "shopping": shopping,

        "receipts": receipts

    }

    with st.spinner("Evaluating claim..."):

        response = requests.post(

            API_URL,

            json=payload

        )

    if response.status_code != 200:

        st.error(response.text)

    else:

        result = response.json()

        st.success("Evaluation Complete")

        st.markdown("---")

        ####################################
        # Decision Summary
        ####################################

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Decision",

                result["decision"]

            )

        with col2:

            st.metric(

                "Approved",

                f"₹ {result['approved_amount']:,.2f}"

            )

        with col3:

            st.metric(

                "Rejected",

                f"₹ {result['rejected_amount']:,.2f}"

            )

        st.markdown("---")

        ####################################
        # Expense Breakdown
        ####################################

        st.subheader("Expense Breakdown")

        df = pd.DataFrame(

            result["expenses"]

        )

        st.dataframe(

            df,

            use_container_width=True

        )

        ####################################
        # Missing Documents
        ####################################

        if result["missing_documents"]:

            st.warning(

                "Missing Documents"

            )

            st.write(

                result["missing_documents"]

            )

        ####################################
        # Policy References
        ####################################

        st.subheader(

            "Policy References"

        )

        for item in result["policy_references"]:

            st.write(

                f"• {item}"

            )

        ####################################
        # Explanation
        ####################################

        st.subheader(

            "AI Explanation"

        )

        st.info(

            result["explanation"]

        )