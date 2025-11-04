"""
Clinic Appointment System - Simplified Version
For Information System Students

This app demonstrates:
- Unit Testing: Test individual calculations (consultation fee, doctor fee, etc.)
- Integration Testing: Test single appointment booking (with components)
- System Testing: Test multiple appointments booking (complete patient record)
"""


class PatientRecord:
    """Patient record to store appointments"""
    
    def __init__(self, patient_id, name):
        self.patient_id = patient_id
        self.name = name
        self.appointments = []  # List to store appointments
    
    def add_appointment(self, doctor, service_type):
        """Add an appointment"""
        appointment = {
            'doctor': doctor,
            'service_type': service_type
        }
        self.appointments.append(appointment)
    
    def get_appointments(self):
        """Get all appointments"""
        return self.appointments


# ========================================
# PART 1: UNIT TESTABLE FUNCTIONS
# Test these functions one by one
# ========================================

def calculate_consultation_fee(service_type):
    """
    Calculate consultation fee based on service type
    
    Service Types:
    - General = Rp 150,000
    - Specialist = Rp 300,000
    - Emergency = Rp 500,000
    """
    service = service_type.lower()
    
    if service == "general":
        return 150_000
    elif service == "specialist":
        return 300_000
    elif service == "emergency":
        return 500_000
    else:
        raise ValueError("Invalid service type")


def calculate_doctor_fee(doctor_level, service_type):
    """
    Calculate doctor fee based on level and service
    
    Doctor Levels:
    - Junior: 50% of consultation fee
    - Senior: 75% of consultation fee
    - Specialist: 100% of consultation fee
    """
    level = doctor_level.lower()
    consultation = calculate_consultation_fee(service_type)
    
    if level == "junior":
        return consultation * 0.5
    elif level == "senior":
        return consultation * 0.75
    elif level == "specialist":
        return consultation * 1.0
    else:
        raise ValueError("Invalid doctor level")


def calculate_time_surcharge(appointment_time):
    """
    Calculate surcharge based on appointment time
    
    Time Surcharge:
    - Morning (06:00-12:00) = No surcharge (0%)
    - Afternoon (12:00-18:00) = 10% surcharge
    - Evening (18:00-21:00) = 25% surcharge
    - Night (21:00-06:00) = 50% surcharge (emergency only)
    """
    hour = int(appointment_time.split(':')[0])
    
    if 6 <= hour < 12:
        return 0.0  # Morning - no surcharge
    elif 12 <= hour < 18:
        return 0.1  # Afternoon - 10%
    elif 18 <= hour < 21:
        return 0.25  # Evening - 25%
    else:
        return 0.5  # Night - 50%


def calculate_insurance_discount(total_fee, insurance_type=None):
    """
    Calculate insurance discount
    
    Insurance Types:
    - BPJS = 80% covered
    - Private = 60% covered
    - Corporate = 70% covered
    - None = 0% (full payment)
    """
    if not insurance_type:
        return 0
    
    insurance = insurance_type.lower()
    
    if insurance == "bpjs":
        discount = total_fee * 0.8
    elif insurance == "private":
        discount = total_fee * 0.6
    elif insurance == "corporate":
        discount = total_fee * 0.7
    else:
        return 0
    
    return discount


def determine_priority(service_type, age):
    """
    Determine patient priority level
    
    Priority Rules:
    - Emergency = "Critical"
    - Specialist + Age >= 60 = "High"
    - Specialist = "Medium"
    - General + Age >= 60 = "Medium"
    - General = "Normal"
    """
    if age < 0:
        raise ValueError("Age cannot be negative")
    
    service = service_type.lower()
    
    if service == "emergency":
        return "Critical"
    elif service == "specialist":
        if age >= 60:
            return "High"
        else:
            return "Medium"
    elif service == "general":
        if age >= 60:
            return "Medium"
        else:
            return "Normal"
    else:
        raise ValueError("Invalid service type")


# ========================================
# PART 2: INTEGRATION FUNCTION
# Book ONE appointment with all components
# ========================================

def book_appointment(patient_name, service_type, doctor_level, appointment_time, insurance_type=None):
    """
    Book ONE appointment with complete fee calculation
    
    Steps:
    1. Calculate consultation fee
    2. Calculate doctor fee
    3. Calculate time surcharge
    4. Calculate total before insurance
    5. Apply insurance discount
    6. Calculate final payment
    
    This is INTEGRATION testing - combines multiple unit functions
    """
    # Validate inputs
    valid_services = ["general", "specialist", "emergency"]
    valid_levels = ["junior", "senior", "specialist"]
    
    if service_type.lower() not in valid_services:
        raise ValueError("Invalid service type")
    if doctor_level.lower() not in valid_levels:
        raise ValueError("Invalid doctor level")
    
    # Calculate base fees
    consultation_fee = calculate_consultation_fee(service_type)
    doctor_fee = calculate_doctor_fee(doctor_level, service_type)
    
    # Calculate surcharge
    surcharge_rate = calculate_time_surcharge(appointment_time)
    base_total = consultation_fee + doctor_fee
    surcharge_amount = base_total * surcharge_rate
    
    # Total before insurance
    total_before_insurance = base_total + surcharge_amount
    
    # Apply insurance
    insurance_discount = calculate_insurance_discount(total_before_insurance, insurance_type)
    final_payment = total_before_insurance - insurance_discount
    
    result = {
        "patient": patient_name,
        "service_type": service_type,
        "doctor_level": doctor_level,
        "appointment_time": appointment_time,
        "consultation_fee": consultation_fee,
        "doctor_fee": doctor_fee,
        "surcharge_rate": surcharge_rate * 100,  # Convert to percentage
        "surcharge_amount": surcharge_amount,
        "total_before_insurance": total_before_insurance,
        "insurance_type": insurance_type,
        "insurance_discount": insurance_discount,
        "final_payment": final_payment
    }
    
    return result


# ========================================
# PART 3: SYSTEM FUNCTION
# Process MULTIPLE appointments for complete patient billing
# ========================================

def process_patient_billing(patient_name, patient_id, appointments_data, patient_age):
    """
    Process complete patient billing with MULTIPLE appointments
    
    This is the MAIN SYSTEM function that does everything:
    1. Book each appointment individually
    2. Determine priority level
    3. Calculate total billing
    4. Create complete billing record
    
    appointments_data format:
    [
        {"service": "General", "doctor": "Junior", "time": "09:00", "insurance": "BPJS"},
        {"service": "Specialist", "doctor": "Senior", "time": "14:00", "insurance": None},
        ...
    ]
    """
    if not appointments_data:
        raise ValueError("Must have at least one appointment")
    
    if patient_age < 0:
        raise ValueError("Age cannot be negative")
    
    # Book each appointment
    booked_appointments = []
    total_consultation = 0
    total_doctor_fee = 0
    total_surcharge = 0
    total_before_insurance = 0
    total_insurance_discount = 0
    
    for apt_data in appointments_data:
        appointment = book_appointment(
            patient_name,
            apt_data["service"],
            apt_data["doctor"],
            apt_data["time"],
            apt_data.get("insurance")
        )
        booked_appointments.append(appointment)
        
        # Accumulate totals
        total_consultation += appointment["consultation_fee"]
        total_doctor_fee += appointment["doctor_fee"]
        total_surcharge += appointment["surcharge_amount"]
        total_before_insurance += appointment["total_before_insurance"]
        total_insurance_discount += appointment["insurance_discount"]
    
    # Calculate final total
    final_total = total_before_insurance - total_insurance_discount
    
    # Determine priority (based on highest priority service)
    priorities = []
    for apt in booked_appointments:
        priority = determine_priority(apt["service_type"], patient_age)
        priorities.append(priority)
    
    # Get highest priority
    priority_order = {"Critical": 4, "High": 3, "Medium": 2, "Normal": 1}
    highest_priority = max(priorities, key=lambda p: priority_order[p])
    
    # Create complete billing record
    record = {
        "patient_id": patient_id,
        "name": patient_name,
        "age": patient_age,
        "priority": highest_priority,
        "appointments": booked_appointments,
        "total_appointments": len(booked_appointments),
        "total_consultation_fee": total_consultation,
        "total_doctor_fee": total_doctor_fee,
        "total_surcharge": total_surcharge,
        "total_before_insurance": total_before_insurance,
        "total_insurance_discount": total_insurance_discount,
        "final_payment": final_total
    }
    
    return record


def print_patient_billing(record):
    """Print complete patient billing nicely"""
    print("\n" + "=" * 70)
    print("PATIENT BILLING RECORD")
    print("=" * 70)
    print(f"Patient ID: {record['patient_id']}")
    print(f"Name: {record['name']}")
    print(f"Age: {record['age']} years")
    print(f"Priority Level: {record['priority']}")
    print("=" * 70)
    
    print("\nAPPOINTMENTS:")
    for i, apt in enumerate(record['appointments'], 1):
        print(f"\n  Appointment #{i}:")
        print(f"    Service: {apt['service_type']}")
        print(f"    Doctor Level: {apt['doctor_level']}")
        print(f"    Time: {apt['appointment_time']}")
        print(f"    Consultation Fee: Rp {apt['consultation_fee']:,}")
        print(f"    Doctor Fee: Rp {apt['doctor_fee']:,.0f}")
        if apt['surcharge_amount'] > 0:
            print(f"    Time Surcharge ({apt['surcharge_rate']:.0f}%): Rp {apt['surcharge_amount']:,.0f}")
        print(f"    Subtotal: Rp {apt['total_before_insurance']:,.0f}")
        if apt['insurance_type']:
            print(f"    Insurance ({apt['insurance_type']}): -Rp {apt['insurance_discount']:,.0f}")
        print(f"    Payment: Rp {apt['final_payment']:,.0f}")
    
    print("\n" + "-" * 70)
    print(f"Total Appointments: {record['total_appointments']}")
    print(f"Total Consultation Fee: Rp {record['total_consultation_fee']:,}")
    print(f"Total Doctor Fee: Rp {record['total_doctor_fee']:,.0f}")
    if record['total_surcharge'] > 0:
        print(f"Total Surcharge: Rp {record['total_surcharge']:,.0f}")
    print(f"Subtotal: Rp {record['total_before_insurance']:,.0f}")
    if record['total_insurance_discount'] > 0:
        print(f"Insurance Discount: -Rp {record['total_insurance_discount']:,.0f}")
    print("-" * 70)
    print(f"FINAL PAYMENT: Rp {record['final_payment']:,.0f}")
    print("=" * 70 + "\n")


def print_appointment_summary(appointment):
    """Print single appointment summary nicely"""
    print("\n" + "=" * 60)
    print(f"APPOINTMENT SUMMARY - {appointment['patient']}")
    print("=" * 60)
    print(f"Service Type: {appointment['service_type']}")
    print(f"Doctor Level: {appointment['doctor_level']}")
    print(f"Time: {appointment['appointment_time']}")
    print("-" * 60)
    print(f"Consultation Fee: Rp {appointment['consultation_fee']:,}")
    print(f"Doctor Fee: Rp {appointment['doctor_fee']:,.0f}")
    if appointment['surcharge_amount'] > 0:
        print(f"Time Surcharge ({appointment['surcharge_rate']:.0f}%): Rp {appointment['surcharge_amount']:,.0f}")
    print(f"Total: Rp {appointment['total_before_insurance']:,.0f}")
    if appointment['insurance_type']:
        print(f"Insurance ({appointment['insurance_type']}): -Rp {appointment['insurance_discount']:,.0f}")
        print(f"Final Payment: Rp {appointment['final_payment']:,.0f}")
    print("=" * 60 + "\n")


# ========================================
# DEMO - How to use the app
# ========================================

def main():
    """Demo of the clinic appointment system"""
    print("=== CLINIC APPOINTMENT SYSTEM DEMO ===\n")
    
    # ============================================
    # INTEGRATION TEST DEMO: Book single appointment
    # ============================================
    print("=" * 70)
    print("INTEGRATION TEST: Single Appointment Booking")
    print("=" * 70)
    
    print("\n--- Appointment 1: Morning General Checkup with BPJS ---")
    apt1 = book_appointment("Budi Santoso", "General", "Junior", "09:00", "BPJS")
    print_appointment_summary(apt1)
    
    print("--- Appointment 2: Afternoon Specialist with Private Insurance ---")
    apt2 = book_appointment("Siti Nurhaliza", "Specialist", "Senior", "14:00", "Private")
    print_appointment_summary(apt2)
    
    print("--- Appointment 3: Evening Emergency without Insurance ---")
    apt3 = book_appointment("Ahmad Wijaya", "Emergency", "Specialist", "19:00", None)
    print_appointment_summary(apt3)
    
    # ============================================
    # SYSTEM TEST DEMO: Complete patient billing with multiple appointments
    # ============================================
    print("\n" + "=" * 70)
    print("SYSTEM TEST: Multiple Appointments - Complete Patient Billing")
    print("=" * 70)
    
    # Patient 1 - Young patient with BPJS (2 appointments)
    print("\n--- PATIENT 1: Dewi Lestari (25 years) - BPJS ---")
    patient1_appointments = [
        {"service": "General", "doctor": "Junior", "time": "08:00", "insurance": "BPJS"},
        {"service": "Specialist", "doctor": "Senior", "time": "10:00", "insurance": "BPJS"}
    ]
    billing1 = process_patient_billing("Dewi Lestari", "P001", patient1_appointments, 25)
    print_patient_billing(billing1)
    
    # Patient 2 - Elderly patient with Corporate insurance (3 appointments)
    print("--- PATIENT 2: Pak Hadi (65 years) - Corporate Insurance ---")
    patient2_appointments = [
        {"service": "General", "doctor": "Senior", "time": "09:00", "insurance": "Corporate"},
        {"service": "Specialist", "doctor": "Specialist", "time": "11:00", "insurance": "Corporate"},
        {"service": "Specialist", "doctor": "Specialist", "time": "15:00", "insurance": "Corporate"}
    ]
    billing2 = process_patient_billing("Pak Hadi", "P002", patient2_appointments, 65)
    print_patient_billing(billing2)
    
    # Patient 3 - Emergency case without insurance (1 appointment)
    print("--- PATIENT 3: Rina Putri (30 years) - Emergency, No Insurance ---")
    patient3_appointments = [
        {"service": "Emergency", "doctor": "Specialist", "time": "20:00", "insurance": None}
    ]
    billing3 = process_patient_billing("Rina Putri", "P003", patient3_appointments, 30)
    print_patient_billing(billing3)
    
    # Patient 4 - Multiple appointments with mixed insurance
    print("--- PATIENT 4: Andi Wijaya (45 years) - Mixed Insurance ---")
    patient4_appointments = [
        {"service": "General", "doctor": "Junior", "time": "08:30", "insurance": "Private"},
        {"service": "Specialist", "doctor": "Senior", "time": "13:00", "insurance": "Private"},
        {"service": "General", "doctor": "Senior", "time": "16:00", "insurance": None}
    ]
    billing4 = process_patient_billing("Andi Wijaya", "P004", patient4_appointments, 45)
    print_patient_billing(billing4)


if __name__ == "__main__":
    main()
