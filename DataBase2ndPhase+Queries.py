import sqlite3

def create_tables(conn):
    """
    Creates the tables in the SQLite database based on the 3NF schema.
    """
    cursor = conn.cursor()

    # Table: Patients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patients (
            p_id INTEGER PRIMARY KEY,
            p_name TEXT,
            p_birthdate TEXT,
            p_phonenumber TEXT,
            p_address TEXT,
            p_gender TEXT,
            i_id INTEGER, -- Foreign key to Insurance
            FOREIGN KEY (i_id) REFERENCES Insurance(i_id)
        )
    ''')

    # Table: MedicalHistory
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MedicalHistory (
            med_history_id INTEGER PRIMARY KEY,
            p_id INTEGER, -- Foreign key to Patients
            had_disease TEXT,
            had_operation TEXT,
            used_med TEXT,
            med_allergy TEXT,
            FOREIGN KEY (p_id) REFERENCES Patients(p_id)
        )
    ''')

    # Table: Dentists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dentists (
            d_id INTEGER PRIMARY KEY,
            d_name TEXT,
            d_specialty TEXT,
            d_phonenumber TEXT,
            d_email TEXT,
            d_medicalid TEXT
        )
    ''')

    # Table: Appointments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Appointments (
            a_id INTEGER PRIMARY KEY,
            p_id INTEGER, -- Foreign key to Patients
            d_id INTEGER, -- Foreign key to Dentists
            a_date TEXT,
            a_time TEXT,
            a_basecost REAL,
            a_descript TEXT,
            FOREIGN KEY (p_id) REFERENCES Patients(p_id),
            FOREIGN KEY (d_id) REFERENCES Dentists(d_id)
        )
    ''')

    # Table: Treatments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Treatments (
            t_id INTEGER PRIMARY KEY,
            t_name TEXT,
            t_cost REAL,
            t_status TEXT,
            material_id INTEGER, -- Foreign key to MaterialsAndEquipment
            diagnosis_id INTEGER, -- Foreign key to Diagnoses
            FOREIGN KEY (material_id) REFERENCES MaterialsAndEquipment(m_id),
            FOREIGN KEY (diagnosis_id) REFERENCES Diagnoses(diagnosis_id)
        )
    ''')

    # Table: Diagnoses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Diagnoses (
            diagnosis_id INTEGER PRIMARY KEY,
            diagnosis_name TEXT,
            recipe TEXT,
            has_xray TEXT, -- 'Yes' or 'No'
            has_bloodtest TEXT -- 'Yes' or 'No'
        )
    ''')

    # Table: Rooms
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rooms (
            r_id INTEGER PRIMARY KEY,
            r_name TEXT,
            r_location TEXT,
            r_capacity INTEGER
        )
    ''')

    # Table: Insurance
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Insurance (
            i_id INTEGER PRIMARY KEY,
            i_type TEXT,
            i_company TEXT,
            i_status TEXT,
            i_percentage REAL
        )
    ''')

    # Table: Payments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Payments (
            pay_id INTEGER PRIMARY KEY,
            p_id INTEGER, -- Foreign key to Patients
            d_id INTEGER, -- Foreign key to Dentists
            a_id INTEGER, -- Foreign key to Appointments
            r_id INTEGER, -- Foreign key to Rooms
            i_id INTEGER, -- Foreign key to Insurance
            pay_date TEXT,
            pay_type TEXT,
            pay_amount REAL,
            pay_tax REAL,
            pay_status TEXT,
            FOREIGN KEY (p_id) REFERENCES Patients(p_id),
            FOREIGN KEY (d_id) REFERENCES Dentists(d_id),
            FOREIGN KEY (a_id) REFERENCES Appointments(a_id),
            FOREIGN KEY (r_id) REFERENCES Rooms(r_id),
            FOREIGN KEY (i_id) REFERENCES Insurance(i_id)
        )
    ''')

    # Table: MaterialsAndEquipment
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MaterialsAndEquipment (
            m_id INTEGER PRIMARY KEY,
            m_quantity INTEGER,
            m_price REAL,
            m_usagedate TEXT,
            m_exp TEXT
        )
    ''')

    # Table: Employees
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            e_id INTEGER PRIMARY KEY,
            e_name TEXT,
            e_role TEXT,
            e_phone TEXT,
            e_salary REAL,
            e_address TEXT,
            e_insurance TEXT -- Could be a foreign key if Insurance table covers employee insurance too
        )
    ''')

    conn.commit()
    print("Tables created successfully!")

def insert_sample_data(conn):
    """
    Inserts sample data into the tables.
    """
    cursor = conn.cursor()

    # Insert data into Insurance
    cursor.execute("INSERT INTO Insurance (i_type, i_company, i_status, i_percentage) VALUES (?, ?, ?, ?)",
                   ('Private', 'HealthCare Inc.', 'Active', 0.80))
    cursor.execute("INSERT INTO Insurance (i_type, i_company, i_status, i_percentage) VALUES (?, ?, ?, ?)",
                   ('Public', 'GovCare', 'Active', 0.50))
    cursor.execute("INSERT INTO Insurance (i_type, i_company, i_status, i_percentage) VALUES (?, ?, ?, ?)",
                   ('None', 'N/A', 'Inactive', 0.00))

    # Insert data into Patients
    cursor.execute("INSERT INTO Patients (p_name, p_birthdate, p_phonenumber, p_address, p_gender, i_id) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Ali Ahmadi', '1990-05-15', '09123456789', 'Tehran, Azadi St.', 'Male', 1))
    cursor.execute("INSERT INTO Patients (p_name, p_birthdate, p_phonenumber, p_address, p_gender, i_id) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Sara Karimi', '1985-11-22', '09301234567', 'Shiraz, Enghelab Ave.', 'Female', 2))
    cursor.execute("INSERT INTO Patients (p_name, p_birthdate, p_phonenumber, p_address, p_gender, i_id) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Reza Moradi', '2000-01-01', '09198765432', 'Isfahan, Vali Asr St.', 'Male', 1))
    cursor.execute("INSERT INTO Patients (p_name, p_birthdate, p_phonenumber, p_address, p_gender, i_id) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Fatemeh Hassani', '1975-03-10', '09101122334', 'Mashhad, Imam Reza Blvd.', 'Female', 3))

    # Insert data into MedicalHistory
    cursor.execute("INSERT INTO MedicalHistory (p_id, had_disease, had_operation, used_med, med_allergy) VALUES (?, ?, ?, ?, ?)",
                   (1, 'None', 'Appendectomy', 'Aspirin', 'Penicillin'))
    cursor.execute("INSERT INTO MedicalHistory (p_id, had_disease, had_operation, used_med, med_allergy) VALUES (?, ?, ?, ?, ?)",
                   (2, 'Diabetes', 'None', 'Metformin', 'None'))
    cursor.execute("INSERT INTO MedicalHistory (p_id, had_disease, had_operation, used_med, med_allergy) VALUES (?, ?, ?, ?, ?)",
                   (3, 'Asthma', 'None', 'Salbutamol', 'None'))

    # Insert data into Dentists
    cursor.execute("INSERT INTO Dentists (d_name, d_specialty, d_phonenumber, d_email, d_medicalid) VALUES (?, ?, ?, ?, ?)",
                   ('Dr. Mohammad Sadeghi', 'General Dentistry', '09121112233', 'sadeghi.m@clinic.com', 'D1001'))
    cursor.execute("INSERT INTO Dentists (d_name, d_specialty, d_phonenumber, d_email, d_medicalid) VALUES (?, ?, ?, ?, ?)",
                   ('Dr. Leila Naseri', 'Orthodontics', '09124445566', 'naseri.l@clinic.com', 'D1002'))
    cursor.execute("INSERT INTO Dentists (d_name, d_specialty, d_phonenumber, d_email, d_medicalid) VALUES (?, ?, ?, ?, ?)",
                   ('Dr. Amir Soltani', 'Oral Surgery', '09127778899', 'soltani.a@clinic.com', 'D1003'))

    # Insert data into Appointments
    cursor.execute("INSERT INTO Appointments (p_id, d_id, a_date, a_time, a_basecost, a_descript) VALUES (?, ?, ?, ?, ?, ?)",
                   (1, 1, '2025-07-01', '10:00', 50.00, 'Routine Checkup'))
    cursor.execute("INSERT INTO Appointments (p_id, d_id, a_date, a_time, a_basecost, a_descript) VALUES (?, ?, ?, ?, ?, ?)",
                   (2, 2, '2025-07-01', '11:00', 75.00, 'Orthodontic Consultation'))
    cursor.execute("INSERT INTO Appointments (p_id, d_id, a_date, a_time, a_basecost, a_descript) VALUES (?, ?, ?, ?, ?, ?)",
                   (3, 1, '2025-07-02', '09:30', 50.00, 'Filling Cavity'))
    cursor.execute("INSERT INTO Appointments (p_id, d_id, a_date, a_time, a_basecost, a_descript) VALUES (?, ?, ?, ?, ?, ?)",
                   (4, 3, '2025-07-03', '14:00', 120.00, 'Tooth Extraction'))

    # Insert data into Diagnoses
    cursor.execute("INSERT INTO Diagnoses (diagnosis_name, recipe, has_xray, has_bloodtest) VALUES (?, ?, ?, ?)",
                   ('Dental Caries', 'Amalgam Filling', 'Yes', 'No'))
    cursor.execute("INSERT INTO Diagnoses (diagnosis_name, recipe, has_xray, has_bloodtest) VALUES (?, ?, ?, ?)",
                   ('Gingivitis', 'Scaling and Root Planing', 'No', 'No'))
    cursor.execute("INSERT INTO Diagnoses (diagnosis_name, recipe, has_xray, has_bloodtest) VALUES (?, ?, ?, ?)",
                   ('Impacted Wisdom Tooth', 'Surgical Extraction', 'Yes', 'Yes'))

    # Insert data into MaterialsAndEquipment
    cursor.execute("INSERT INTO MaterialsAndEquipment (m_quantity, m_price, m_usagedate, m_exp) VALUES (?, ?, ?, ?)",
                   (100, 5.50, '2025-06-15', '2026-12-31'))
    cursor.execute("INSERT INTO MaterialsAndEquipment (m_quantity, m_price, m_usagedate, m_exp) VALUES (?, ?, ?, ?)",
                   (50, 12.00, '2025-06-10', '2027-06-30'))
    cursor.execute("INSERT INTO MaterialsAndEquipment (m_quantity, m_price, m_usagedate, m_exp) VALUES (?, ?, ?, ?)",
                   (20, 25.00, '2025-05-20', '2028-01-01'))

    # Insert data into Treatments
    cursor.execute("INSERT INTO Treatments (t_name, t_cost, t_status, material_id, diagnosis_id) VALUES (?, ?, ?, ?, ?)",
                   ('Filling', 150.00, 'Completed', 1, 1))
    cursor.execute("INSERT INTO Treatments (t_name, t_cost, t_status, material_id, diagnosis_id) VALUES (?, ?, ?, ?, ?)",
                   ('Scaling', 100.00, 'Completed', 2, 2))
    cursor.execute("INSERT INTO Treatments (t_name, t_cost, t_status, material_id, diagnosis_id) VALUES (?, ?, ?, ?, ?)",
                   ('Extraction', 300.00, 'Pending', 3, 3))

    # Insert data into Rooms
    cursor.execute("INSERT INTO Rooms (r_name, r_location, r_capacity) VALUES (?, ?, ?)",
                   ('Room A', 'First Floor', 1))
    cursor.execute("INSERT INTO Rooms (r_name, r_location, r_capacity) VALUES (?, ?, ?)",
                   ('Room B', 'First Floor', 1))
    cursor.execute("INSERT INTO Rooms (r_name, r_location, r_capacity) VALUES (?, ?, ?)",
                   ('Surgery Room 1', 'Second Floor', 2))

    # Insert data into Employees
    cursor.execute("INSERT INTO Employees (e_name, e_role, e_phone, e_salary, e_address, e_insurance) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Fatemeh Rezvani', 'Receptionist', '09109998877', 3000.00, 'Tehran, Vanak Sq.', 'HealthCare Inc.'))
    cursor.execute("INSERT INTO Employees (e_name, e_role, e_phone, e_salary, e_address, e_insurance) VALUES (?, ?, ?, ?, ?, ?)",
                   ('Hassan Ahmadi', 'Dental Assistant', '09106665544', 2500.00, 'Shiraz, Zand St.', 'GovCare'))

    # Insert data into Payments
    cursor.execute("INSERT INTO Payments (p_id, d_id, a_id, r_id, i_id, pay_date, pay_type, pay_amount, pay_tax, pay_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (1, 1, 1, 1, 1, '2025-07-01', 'Credit Card', 50.00 * (1 - 0.80), 0.00, 'Successful')) # Patient 1, Dr. 1, Appt 1, Room 1, Insurance 1
    cursor.execute("INSERT INTO Payments (p_id, d_id, a_id, r_id, i_id, pay_date, pay_type, pay_amount, pay_tax, pay_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (2, 2, 2, 2, 2, '2025-07-01', 'Cash', 75.00 * (1 - 0.50), 0.00, 'Successful')) # Patient 2, Dr. 2, Appt 2, Room 2, Insurance 2
    cursor.execute("INSERT INTO Payments (p_id, d_id, a_id, r_id, i_id, pay_date, pay_type, pay_amount, pay_tax, pay_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (4, 3, 4, 3, 3, '2025-07-03', 'Bank Transfer', 120.00, 0.05 * 120.00, 'Pending')) # Patient 4, Dr. 3, Appt 4, Room 3, Insurance 3 (No discount)

    conn.commit()
    print("Sample data inserted successfully!")

def get_all_patients(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patients")
    return cursor.fetchall()

def get_patient_by_id(conn, p_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patients WHERE p_id = ?", (p_id,))
    return cursor.fetchone()

def add_new_patient(conn, name, birthdate, phonenumber, address, gender, insurance_id):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Patients (p_name, p_birthdate, p_phonenumber, p_address, p_gender, i_id) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, birthdate, phonenumber, address, gender, insurance_id))
        conn.commit()
        print(f"Patient {name} added successfully!")
    except sqlite3.Error as e:
        print(f"Error adding patient: {e}")

def update_patient_phone(conn, p_id, new_phone):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Patients SET p_phonenumber = ? WHERE p_id = ?", (new_phone, p_id))
        conn.commit()
        print(f"Patient {p_id} phone number updated to {new_phone}.")
    except sqlite3.Error as e:
        print(f"Error updating patient phone: {e}")

def delete_patient(conn, p_id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Patients WHERE p_id = ?", (p_id,))
        conn.commit()
        print(f"Patient {p_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting patient: {e}")

# You would implement similar CRUD functions for other tables (Dentists, Appointments, etc.)

def run_queries(conn):
    """
    Executes and prints results for 20 sample SQL queries.
    """
    cursor = conn.cursor()
    queries = [
        # 1. Select all patients and their insurance company
        ("SELECT p.p_name, i.i_company FROM Patients p JOIN Insurance i ON p.i_id = i.i_id", "Patients with their Insurance Companies"),

        # 2. Find all appointments for a specific dentist (e.g., Dr. Mohammad Sadeghi)
        ("SELECT p.p_name, a.a_date, a.a_time FROM Appointments a JOIN Patients p ON a.p_id = p.p_id JOIN Dentists d ON a.d_id = d.d_id WHERE d.d_name = 'Dr. Mohammad Sadeghi'", "Appointments for Dr. Mohammad Sadeghi"),

        # 3. Get the total cost of all completed treatments
        ("SELECT SUM(t_cost) FROM Treatments WHERE t_status = 'Completed'", "Total Cost of Completed Treatments"),

        # 4. List all materials with an expiry date before a specific date (e.g., 2027-01-01)
        ("SELECT m_id, m_quantity, m_exp FROM MaterialsAndEquipment WHERE m_exp < '2027-01-01'", "Materials expiring before 2027-01-01"),

        # 5. Find patients who have a specific medical allergy (e.g., Penicillin)
        ("SELECT p.p_name FROM Patients p JOIN MedicalHistory mh ON p.p_id = mh.p_id WHERE mh.med_allergy = 'Penicillin'", "Patients allergic to Penicillin"),

        # 6. Count the number of appointments per dentist
        ("SELECT d.d_name, COUNT(a.a_id) FROM Dentists d LEFT JOIN Appointments a ON d.d_id = a.d_id GROUP BY d.d_name", "Number of Appointments per Dentist"),

        # 7. List all diagnoses that required an X-ray
        ("SELECT diagnosis_name FROM Diagnoses WHERE has_xray = 'Yes'", "Diagnoses requiring X-ray"),

        # 8. Get the details of payments made by 'Credit Card'
        ("SELECT p.p_name, pay.pay_date, pay.pay_amount FROM Payments pay JOIN Patients p ON pay.p_id = p.p_id WHERE pay.pay_type = 'Credit Card'", "Payments made by Credit Card"),

        # 9. Find employees with a salary greater than 2800
        ("SELECT e_name, e_role, e_salary FROM Employees WHERE e_salary > 2800", "Employees with salary > 2800"),

        # 10. List patients who have no insurance
        ("SELECT p_name FROM Patients WHERE i_id IN (SELECT i_id FROM Insurance WHERE i_status = 'Inactive')", "Patients with no active insurance"),

        # 11. Get the average base cost of appointments
        ("SELECT AVG(a_basecost) FROM Appointments", "Average Appointment Base Cost"),

        # 12. Find the most expensive treatment
        ("SELECT t_name, t_cost FROM Treatments ORDER BY t_cost DESC LIMIT 1", "Most Expensive Treatment"),

        # 13. List all rooms and their capacities
        ("SELECT r_name, r_capacity FROM Rooms", "All Rooms and their Capacities"),

        # 14. Get the total quantity of a specific material (e.g., material_id = 1)
        ("SELECT m_quantity FROM MaterialsAndEquipment WHERE m_id = 1", "Quantity of Material ID 1"),

        # 15. Find patients born after 1995
        ("SELECT p_name, p_birthdate FROM Patients WHERE p_birthdate > '1995-12-31'", "Patients born after 1995"),

        # 16. List treatments that are 'Pending'
        ("SELECT t_name, t_cost FROM Treatments WHERE t_status = 'Pending'", "Pending Treatments"),

        # 17. Get the contact details of dentists specializing in 'Orthodontics'
        ("SELECT d_name, d_phonenumber, d_email FROM Dentists WHERE d_specialty = 'Orthodontics'", "Orthodontics Specialists Contact Details"),

        # 18. Find the total amount of payments with tax
        ("SELECT SUM(pay_amount + pay_tax) FROM Payments WHERE pay_status = 'Successful'", "Total Successful Payments (including tax)"),

        # 19. List patients who have had an operation
        ("SELECT p.p_name FROM Patients p JOIN MedicalHistory mh ON p.p_id = mh.p_id WHERE mh.had_operation IS NOT NULL AND mh.had_operation != 'None'", "Patients who had an operation"),

        # 20. Get the average salary of employees
        ("SELECT AVG(e_salary) FROM Employees", "Average Employee Salary")
    ]

    for i, (query, description) in enumerate(queries):
        print(f"\n--- Query {i+1}: {description} ---")
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                # Print column names (simple approach)
                col_names = [description[0] for description in cursor.description]
                print(col_names)
                for row in results:
                    print(row)
            else:
                print("No results found.")
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

def main_menu():
    print("\n--- Dental Clinic Database Management System ---")
    print("1. Add New Patient")
    print("2. View All Patients")
    print("3. Find Patient by ID")
    print("4. Update Patient Phone Number")
    print("5. Delete Patient")
    print("6. Run Sample SQL Queries")
    print("7. Exit")

def main():
    db_name = 'dental_clinic.db'
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        create_tables(conn)
        insert_sample_data(conn) # Insert sample data on first run or if tables are empty

        while True:
            main_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter patient name: ")
                birthdate = input("Enter patient birthdate (YYYY-MM-DD): ")
                phonenumber = input("Enter patient phone number: ")
                address = input("Enter patient address: ")
                gender = input("Enter patient gender: ")
                insurance_id = int(input("Enter insurance ID: "))
                add_new_patient(conn, name, birthdate, phonenumber, address, gender, insurance_id)
            elif choice == '2':
                patients = get_all_patients(conn)
                if patients:
                    print("\n--- All Patients ---")
                    for patient in patients:
                        print(patient)
                else:
                    print("No patients found.")
            elif choice == '3':
                p_id = int(input("Enter patient ID: "))
                patient = get_patient_by_id(conn, p_id)
                if patient:
                    print("\n--- Patient Details ---")
                    print(patient)
                else:
                    print("Patient not found.")
            elif choice == '4':
                p_id = int(input("Enter patient ID to update: "))
                new_phone = input("Enter new phone number: ")
                update_patient_phone(conn, p_id, new_phone)
            elif choice == '5':
                p_id = int(input("Enter patient ID to delete: "))
                delete_patient(conn, p_id)
            elif choice == '6':
                run_queries(conn)
            elif choice == '7':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()    