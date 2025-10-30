import os
import streamlit as st
import requests
from fpdf import FPDF

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="HolidayPlanner", layout="wide")
st.title("🌴 Holiday Planner")

# ===== Form =====
with st.form("planner_form"):
    destination = st.text_input("Destination", "")
    budget = st.number_input("Budget (USD)", min_value=50.0, value=500.0)
    duration = st.number_input("Duration (days)", min_value=1, max_value=30, value=5)
    submitted = st.form_submit_button("Plan my trip")

if submitted:
    if not destination:
        st.warning("Please enter a destination.")
    else:
        try:
            with st.spinner("✨ Planning your trip..."):
                resp = requests.post(
                    f"{API_URL}/plan/",
                    params={"destination": destination, "budget": budget, "duration": duration},
                    timeout=60,
                )
                resp.raise_for_status()
                data = resp.json()

            plan = data.get("plan", {})
            st.success("✅ Plan created successfully!")

            # ---- Weather ----
            weather = plan.get("weather", {})
            st.subheader("🌤️ Weather Overview")
            st.write(f"**Description:** {weather.get('description', '-')}")
            st.write(f"**Temperature:** {weather.get('temperature', '-')}")
            st.write(f"**Humidity:** {weather.get('humidity', '-')}%")

            # ---- Places ----
            st.subheader("🏛️ Recommended Places")
            col1, col2, col3 = st.columns(3)
            for col, title, key in zip(
                (col1, col2, col3), 
                ("Museums", "Food / Restaurants", "Culture / Activities"), 
                ("museums", "food", "culture")
            ):
                with col:
                    st.markdown(f"**{title}**")
                    for item in plan.get("places", {}).get(key, []):
                        st.write(f"- {item}")

            # ---- Itinerary ----
            st.subheader("🗓️ Trip Itinerary")
            st.markdown(plan.get("itinerary", "_No itinerary generated._"))

            # ---- Budget ----
            st.subheader("💰 Budget Overview")
            budget_info = plan.get("budget", {})
            st.write(f"**Estimate:** {budget_info.get('estimate', '-')}")
            st.write(f"**Status:** {budget_info.get('flag', '-')}")

            # ---- Evaluation ----
            st.subheader("✅ Plan Evaluation")
            evaluation = plan.get("evaluation", {})
            st.write(f"**Status:** {evaluation.get('status', '-')}")
            for alert in evaluation.get("alerts", []):
                st.warning(alert)

            # ---- PDF Export ----
            if st.button("📄 Export as PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, f"Holiday Plan - {destination}", ln=True)
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 8, plan.get("summary", ""))

                pdf.ln(5)
                pdf.cell(0, 10, f"Weather: {weather.get('description', '-')}, {weather.get('temperature', '-')}", ln=True)
                pdf.cell(0, 10, f"Budget: {budget_info.get('estimate', '-')} ({budget_info.get('flag', '-')})", ln=True)

                pdf.ln(10)
                pdf.multi_cell(0, 8, f"Itinerary:\n{plan.get('itinerary', '')}")

                pdf.output("holiday_plan.pdf")
                st.success("📄 PDF saved as `holiday_plan.pdf` in the project folder!")

        except Exception as e:
            st.error(f"Error: {e}")
