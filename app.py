# =============================================================================
# CLINIC APPOINTMENT MANAGEMENT SYSTEM (FRONTEND GUI)
# Tasks: e) Streamlit GUI, f) Exception Handling & Validation
# =============================================================================

import streamlit as st
import clinic_logic

st.set_page_config(
    page_title="Clinic Appointment Management System",
    layout="centered"
)

st.title("Clinic Appointment Management System")
st.markdown("Register patient appointments, evaluate symptom urgency, and calculate payable consultation fees.")

st.divider()

# --- e) GUI DEVELOPMENT: INPUT FIELDS & USER EVENTS ---

st.subheader("Patient Registration & Consultation Details")

patient_id = st.text_input("Patient ID", placeholder="e.g., P-1001")
patient_name = st.text_input("Patient Full Name", placeholder="e.g., Ali bin Ahmad")

gender = st.selectbox(
    "Gender",
    options=["Lelaki", "Perempuan"]
)

age_input = st.text_input("Age (Years)", placeholder="e.g., 35")

symptoms = st.text_area("Symptoms Description", placeholder="e.g., Sakit dada dan sesak nafas")

doctor_fee_input = st.text_input("Doctor Base Fee (RM)", placeholder="e.g., 100.00")

# User Event 1: Priority / Senior Discount Toggle
has_discount = st.checkbox("Apply Senior / Special Discount (10%)")

# User Event 2: Insurance Coverage Slider
insurance_rate = st.slider("Insurance Coverage (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0)

st.divider()

# --- e) PROCESS BUTTON & f) EXCEPTION HANDLING ---

# User Event 3: Processing Action Button
if st.button("Process Appointment", type="primary"):
    
    has_error = False

    # Validation 1: Detect empty required fields
    if not patient_id.strip():
        st.error("Error: Patient ID field cannot be empty.")
        has_error = True

    if not patient_name.strip():
        st.error("Error: Patient Name field cannot be empty.")
        has_error = True

    if not symptoms.strip():
        st.error("Error: Symptoms Description field cannot be empty.")
        has_error = True

    if not age_input.strip():
        st.error("Error: Age field cannot be empty.")
        has_error = True

    if not doctor_fee_input.strip():
        st.error("Error: Doctor Base Fee field cannot be empty.")
        has_error = True

    # Validation 2: Validate numerical input for Age
    valid_age = 0
    if age_input.strip():
        try:
            valid_age = int(age_input)
            if valid_age <= 0 or valid_age > 120:
                st.error("Input Error: Age must be a positive integer between 1 and 120.")
                has_error = True
        except ValueError:
            st.error("Type Error: Age must be a valid whole number.")
            has_error = True

    # Validation 3: Validate numerical input for Doctor Fee
    valid_fee = 0.0
    if doctor_fee_input.strip():
        try:
            valid_fee = float(doctor_fee_input)
            if valid_fee <= 0:
                st.error("Input Error: Doctor Fee must be greater than RM 0.00.")
                has_error = True
        except ValueError:
            st.error("Type Error: Doctor Fee must be a valid numerical value (e.g., 80.00).")
            has_error = True

    # System Execution using try-except for unexpected errors
    if not has_error:
        try:
            discount_percentage = 10.0 if has_discount else 0.0

            # Instantiate Subclass Object (Task d)
            patient_obj = clinic_logic.PriorityPatient(
                patient_id=patient_id.strip(),
                name=patient_name.strip(),
                age=valid_age,
                gender=gender,
                insurance_coverage=insurance_rate
            )

            # Operations via imported module (Tasks a & c)
            urgency = clinic_logic.determine_urgency_status(symptoms)
            final_fee = patient_obj.calculate_final_fee(valid_fee, discount_percentage)

            st.success("Appointment Successfully Processed!")
            st.subheader("Appointment Summary")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Patient Info", patient_obj.get_patient_info())
                st.metric("Urgency Level", urgency)
                st.metric("Base Doctor Fee", f"RM {valid_fee:.2f}")

            with col2:
                st.metric("Applied Discount", f"{discount_percentage}%")
                st.metric("Insurance Coverage", f"{insurance_rate}%")
                st.metric("Final Payable Fee", f"RM {final_fee:.2f}")

            st.divider()
            
            if urgency == "KECEMASAN / SEGERA":
                st.warning("Attention: Emergency symptoms detected. Direct patient to triage room immediately.")
            else:
                st.info("Status: Normal queue assignment.")

        except Exception as e:
            st.error(f"An unexpected system error occurred: {str(e)}")