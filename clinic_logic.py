# =============================================================================
# CLINIC APPOINTMENT MANAGEMENT SYSTEM (BACKEND MODULE)
# Tasks: a) Functions, b) Class & Object, c) Module, d) Inheritance
# =============================================================================

# --- a) FUNCTION IMPLEMENTATION ---

def calculate_appointment_fee(base_fee, discount_rate):
    """Function 1: Calculates total fee after discount."""
    discount_amount = base_fee * (discount_rate / 100)
    return base_fee - discount_amount


def determine_urgency_status(symptoms_description):
    """Function 2: Determines patient urgency priority based on symptoms."""
    symptoms_description = symptoms_description.lower()
    high_risk_keywords = ["dada", "sesak", "pingsan", "pendarahan", "sakit kepala teruk"]
    
    for word in high_risk_keywords:
        if word in symptoms_description:
            return "KECEMASAN / SEGERA"
    
    return "BIASA (Normal)"


# --- b) CLASS AND OBJECT IMPLEMENTATION ---

class Patient:
    """Parent Class representing a clinic patient."""
    def __init__(self, patient_id, name, age, gender):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender

    def get_patient_info(self):
        """Method 1: Displays and returns patient profile information."""
        return f"[ID: {self.patient_id}] {self.name} ({self.gender}, {self.age} years)"

    def calculate_consultation_fee(self, doctor_fee):
        """Method 2: Calculates base consultation fee."""
        return float(doctor_fee)


# --- d) APPLY INHERITANCE FEATURES ---

class PriorityPatient(Patient):
    """Subclass inheriting from Patient, adding insurance and priority features."""
    def __init__(self, patient_id, name, age, gender, insurance_coverage):
        super().__init__(patient_id, name, age, gender)
        self.insurance_coverage = insurance_coverage

    def calculate_final_fee(self, doctor_fee, discount_rate=0.0):
        """Overridden/Extended Method: Calculates fee with insurance coverage applied."""
        base_consultation = self.calculate_consultation_fee(doctor_fee)
        after_discount = calculate_appointment_fee(base_consultation, discount_rate)
        
        coverage_amount = after_discount * (self.insurance_coverage / 100)
        final_payable = after_discount - coverage_amount
        return final_payable