import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as conn
from datetime import date


class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Tracker v1.2")
        self.root.geometry("850x650") 
        self.root.configure(bg='#f0f0f0')
        
        try:
            self.db = conn.connect(
                host="localhost",
                user="root",
                password="Password",
                database="attendance_db"
            )
            self.cursor = self.db.cursor()
            messagebox.showinfo("DB Status", "Connected to database!")
        except Exception as e:
            messagebox.showerror("Oops!", f"Database connection failed: {str(e)}")
            return
        
        self.setup_ui() 
    
    def setup_ui(self):
        title = tk.Label(
            self.root, 
            text="Employee Attendance System", 
            font=("Comic Sans MS", 18, "bold"),
            bg='#f0f0f0',
            fg='#34495e'
        )
        title.pack(pady=15)
        
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill='both', expand=True, padx=15, pady=10)
        
        self.tab1 = ttk.Frame(self.tabs)  # add employee
        self.tab2 = ttk.Frame(self.tabs)  # attendance   
        self.tab3 = ttk.Frame(self.tabs)  # records
        
        self.tabs.add(self.tab1, text="Add Employee")
        self.tabs.add(self.tab2, text="Mark Attendance") 
        self.tabs.add(self.tab3, text="View Records")
        
        self.build_add_tab()
        self.build_attendance_tab()
        self.build_view_tab()
    
    def build_add_tab(self):
        main_frame = ttk.LabelFrame(self.tab1, text="Add New Employee", padding=25)
        main_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Employee name input
        tk.Label(main_frame, text="Name:", font=("Arial", 11)).grid(row=0, column=0, sticky='w', pady=8)
        self.name_box = ttk.Entry(main_frame, font=("Arial", 11), width=35)  # made it wider
        self.name_box.grid(row=0, column=1, padx=15, pady=8)
        
        # Department input
        tk.Label(main_frame, text="Department:", font=("Arial", 11)).grid(row=1, column=0, sticky='w', pady=8)
        self.dept_box = ttk.Entry(main_frame, font=("Arial", 11), width=35)
        self.dept_box.grid(row=1, column=1, padx=15, pady=8)
        
        # Submit button
        submit_btn = tk.Button(
            main_frame, 
            text="Add Employee", 
            command=self.add_new_employee,
            bg='#3498db',
            fg='white',
            font=("Arial", 11, "bold"),
            relief='flat',
            padx=20
        )
        submit_btn.grid(row=2, column=0, columnspan=2, pady=25)
        
        main_frame.columnconfigure(1, weight=1)
    
    def build_attendance_tab(self):
        container = ttk.LabelFrame(self.tab2, text="Mark Daily Attendance", padding=25)
        container.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Employee ID input  
        tk.Label(container, text="Employee ID:", font=("Arial", 11)).grid(row=0, column=0, sticky='w', pady=8)
        self.id_input = ttk.Entry(container, font=("Arial", 11), width=35)
        self.id_input.grid(row=0, column=1, padx=15, pady=8)
        
        # Status dropdown
        tk.Label(container, text="Attendance:", font=("Arial", 11)).grid(row=1, column=0, sticky='w', pady=8)
        self.attendance_status = tk.StringVar(value="Present")
        status_dropdown = ttk.Combobox(
            container, 
            textvariable=self.attendance_status,
            values=["Present", "Absent"],
            state="readonly",
            font=("Arial", 11),
            width=33
        )
        status_dropdown.grid(row=1, column=1, padx=15, pady=8)
        

        tk.Label(container, text="Date:", font=("Arial", 11)).grid(row=2, column=0, sticky='w', pady=8)
        todays_date = date.today().strftime("%B %d, %Y")  
        date_display = tk.Label(container, text=todays_date, font=("Arial", 11, "italic"), fg='#7f8c8d')
        date_display.grid(row=2, column=1, padx=15, pady=8, sticky='w')
        
        # Mark attendance button
        mark_button = tk.Button(
            container, 
            text="Mark Attendance", 
            command=self.mark_todays_attendance,
            bg='#27ae60',
            fg='white',
            font=("Arial", 11, "bold"),
            relief='flat',
            padx=20
        )
        mark_button.grid(row=3, column=0, columnspan=2, pady=25)
        
        ref_frame = ttk.LabelFrame(container, text="Employee Reference", padding=15)
        ref_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=15)
        
        self.employee_list = tk.Listbox(ref_frame, height=6, font=("Courier", 9))
        list_scroll = ttk.Scrollbar(ref_frame, orient='vertical', command=self.employee_list.yview)
        self.employee_list.configure(yscrollcommand=list_scroll.set)
        
        self.employee_list.pack(side='left', fill='both', expand=True)
        list_scroll.pack(side='right', fill='y')
        
        # Refresh list button
        refresh_list_btn = tk.Button(ref_frame, text="Refresh", command=self.load_employee_list, 
                                   bg='#95a5a6', fg='white', relief='flat')
        refresh_list_btn.pack(pady=8)
        
        container.columnconfigure(1, weight=1)
        ref_frame.columnconfigure(0, weight=1)
    
    def build_view_tab(self):
        # attendance
        view_container = ttk.LabelFrame(self.tab3, text="Attendance History", padding=25)
        view_container.pack(fill='both', expand=True, padx=25, pady=25)
        
        table_columns = ('Employee', 'Date', 'Status') 
        self.records_table = ttk.Treeview(view_container, columns=table_columns, show='headings', height=18)
        
        self.records_table.heading('Employee', text='Employee Name')
        self.records_table.heading('Date', text='Date')
        self.records_table.heading('Status', text='Attendance Status')
        
        self.records_table.column('Employee', width=250)
        self.records_table.column('Date', width=120)
        self.records_table.column('Status', width=150)
        
        vert_scroll = ttk.Scrollbar(view_container, orient='vertical', command=self.records_table.yview)
        horiz_scroll = ttk.Scrollbar(view_container, orient='horizontal', command=self.records_table.xview)
        
        self.records_table.configure(yscrollcommand=vert_scroll.set, xscrollcommand=horiz_scroll.set)
        
        # Place table and scrollbars
        self.records_table.grid(row=0, column=0, sticky='nsew')
        vert_scroll.grid(row=0, column=1, sticky='ns')
        horiz_scroll.grid(row=1, column=0, sticky='ew')
        
        refresh_data_btn = tk.Button(view_container, text="Refresh Data", command=self.load_attendance_data,
                                   bg='#e67e22', fg='white', font=("Arial", 10, "bold"), relief='flat')
        refresh_data_btn.grid(row=2, column=0, pady=15)
        
        view_container.grid_rowconfigure(0, weight=1)
        view_container.grid_columnconfigure(0, weight=1)
        
        self.load_attendance_data()
    
    def add_new_employee(self):
        emp_name = self.name_box.get().strip()
        emp_dept = self.dept_box.get().strip()
        
        if not emp_name or not emp_dept:
            messagebox.showerror("Missing Info", "Please fill out both name and department!")
            return
        
        # Insert into database
        try:
            insert_query = "INSERT INTO employee(name, dept) VALUES (%s, %s)"
            self.cursor.execute(insert_query, (emp_name, emp_dept))
            self.db.commit() 
            
            messagebox.showinfo("Success!", f"Added {emp_name} to the system!")
            
            self.name_box.delete(0, tk.END)
            self.dept_box.delete(0, tk.END)
            
            self.load_employee_list()
            
        except Exception as error:
            messagebox.showerror("Database Error", f"Failed to add employee: {str(error)}")
    
    def mark_todays_attendance(self):
        employee_id = self.id_input.get().strip()
        status = self.attendance_status.get()
        
        if not employee_id:
            messagebox.showerror("Missing Info", "Please enter an Employee ID!")
            return
        
        try:
            verify_query = "SELECT name FROM employee WHERE emp_id = %s"
            self.cursor.execute(verify_query, (employee_id,))
            employee_data = self.cursor.fetchone()
            
            if not employee_data:
                messagebox.showerror("Not Found", f"Employee ID {employee_id} doesn't exist!")
                return
            
            today = date.today()
            duplicate_check = "SELECT * FROM attendance WHERE emp_id = %s AND date = %s"
            self.cursor.execute(duplicate_check, (employee_id, today))
            existing_entry = self.cursor.fetchone()
            
            if existing_entry:
                update_choice = messagebox.askyesno(
                    "Already Marked", 
                    f"Attendance for {employee_data[0]} is already marked today. Update it?"
                )
                if update_choice:
                    # Update existing record
                    update_query = "UPDATE attendance SET status = %s WHERE emp_id = %s AND date = %s"
                    self.cursor.execute(update_query, (status, employee_id, today))
                    self.db.commit()
                    messagebox.showinfo("Updated!", f"Updated attendance for {employee_data[0]}!")
                return
            
            # Insert new attendance record
            attendance_query = "INSERT INTO attendance(emp_id, date, status) VALUES (%s, %s, %s)"
            self.cursor.execute(attendance_query, (employee_id, today, status))
            self.db.commit()
            
            messagebox.showinfo("Marked!", f"Attendance marked for {employee_data[0]}!")
            
            self.id_input.delete(0, tk.END)
            
            if self.tabs.index(self.tabs.select()) == 2:
                self.load_attendance_data()
            
        except Exception as error:
            messagebox.showerror("Database Error", f"Error marking attendance: {str(error)}")
    
    def load_attendance_data(self):
        for item in self.records_table.get_children():
            self.records_table.delete(item)
        
        try:
            data_query = """
                SELECT employee.name, attendance.date, attendance.status 
                FROM attendance 
                JOIN employee ON attendance.emp_id = employee.emp_id 
                ORDER BY attendance.date DESC, employee.name ASC
            """
            self.cursor.execute(data_query)
            all_records = self.cursor.fetchall()
            
            if not all_records:
                self.records_table.insert('', 'end', values=('No attendance records yet', '', ''))
            else:
                for record in all_records:
                    self.records_table.insert('', 'end', values=record)
            
        except Exception as error:
            messagebox.showerror("Database Error", f"Error loading attendance data: {str(error)}")
    
    def load_employee_list(self):
        self.employee_list.delete(0, tk.END)
        
        try:
            # Get all employees
            emp_query = "SELECT emp_id, name, dept FROM employee ORDER BY emp_id"
            self.cursor.execute(emp_query)
            all_employees = self.cursor.fetchall()
            
            if all_employees:
                for emp in all_employees:
                    display_text = f"ID: {emp[0]:2} | {emp[1]:15} | {emp[2]}"  
                    self.employee_list.insert(tk.END, display_text)
            else:
                self.employee_list.insert(tk.END, "No employees added yet")
                
        except Exception as error:
            messagebox.showerror("Database Error", f"Error loading employee list: {str(error)}")
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

def run_app():
    root = tk.Tk()
    
    style = ttk.Style()
    style.theme_use('clam')  
    
    #app
    app = AttendanceSystem(root)
    
    def close_app():
        if hasattr(app, 'db'):
            app.db.close()  # close database connection
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", close_app)
    
    root.mainloop()

if __name__ == "__main__":
    run_app()
