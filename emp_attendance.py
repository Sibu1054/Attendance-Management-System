import mysql.connector as conn
from datetime import date

db = conn.connect(
    host="localhost",
    user="root",
    password="Here type your database password",
    database="attendance_db"
)
cursor = db.cursor()

def add_employees(name,dept):
    query = "INSERT INTO employee(name,dept) VALUES (%s,%s)"
    cursor.execute(query,(name,dept))
    db.commit()
    print(f"Employee '{name}' added successfully!")

def mark_attendance(emp_id,status):
    today = date.today()
    query = "INSERT INTO attendance(emp_id,date,status) VALUES (%s,%s,%s)"
    cursor.execute(query,(emp_id,today,status))
    db.commit()
    print(f"Attendance marked for Employee ID {emp_id}.")

def view_attendance():
    cursor.execute("""SELECT employee.name, attendance.date,attendance.status FROM attendance 
    JOIN employee ON attendance.emp_id = employee.emp_id
    ORDER BY attendance.date DESC""")
    records = cursor.fetchall()
    if not records:
        print("No attendance records found!")
    else:
        for row in records:
            print(f"ID: {row[0]} | Name : {row[1]} | Dept: {row[2]} | Date : {row[3]} | Status : {row[4]}")
    

# MENU
while True:
    print("\n--- Employee Attendance System ---")
    print("1. Add Employee")
    print("2. Mark Attendance")
    print("3. View Attendance")
    print("4. Exit")

    choice = input("Enter Choice: ")
    if choice == '1':
        name = input("Enter employee name: ")
        dept = input("Enter dept: ")
        add_employees(name,dept)
    
    elif choice == '2':
        emp_id = input("Enter employee ID: ")
        status = input("Enter status (Present/Absent): ")
        mark_attendance(emp_id,status)
    
    elif choice == '3':
        view_attendance()

    elif choice == '4':
        break
    else:
        print("Invalid choice,try again")
