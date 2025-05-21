from flask import Flask, render_template ,request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime, timedelta, date
import calendar

app = Flask(__name__)
app.secret_key = 'fahad-1234xyz'

# ✅ Using mysql+mysqlconnector (correct dialect)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3307/office_management_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




@app.route('/')
def home():

    query=text('select COUNT(*) from department')
    dept_no = db.session.execute(query).scalar() 

    query=text('select COUNT(*) from employee')
    employee_no = db.session.execute(query).scalar() 

    return render_template('home.html',total_departments=dept_no,total_employees=employee_no)

@app.route('/employees', methods=['GET', 'POST'])
def employee():
    employee_data = None
    searched = False

    if request.method == 'POST':
        emp_id = request.form['emp-id']
        searched = True

        try:
            query = text("SELECT EmpNo, name, address, phone_number, Department_ID, manager_id FROM employee WHERE EmpNo = :emp_id")
            result = db.session.execute(query, {'emp_id': emp_id}).fetchone()

            #getting department info of relevant employee
            dept_id=result[4]
            query2=text('select name,area from department where deptid = :dept_id')
            result2 = db.session.execute(query2, {'dept_id': dept_id}).fetchone()

            if result:
                employee_data = {
                    'EmpNo': result[0],
                    'name': result[1],
                    'address': result[2],
                    'phone': result[3],
                    'dept': result[4],
                    'manager': result[5],
                    'dept_name': result2[0],
                    'dept_area': result2[1]
                }

        except Exception as e:
            print("Error fetching employee data:",e)

    return render_template('employees.html', employee=employee_data, searched=searched)

    #return render_template('employees.html', employees=employees, css_file='css/employees.css')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    attendance = None

    if request.method == 'POST':
        emp_id = request.form['employee_id']

        try:
            # Get employee name
            emp_name_query = text("SELECT name FROM employee WHERE EmpNo = :emp_id")
            emp_name_result = db.session.execute(emp_name_query, {'emp_id': emp_id}).fetchone()

            if emp_name_result:
                employee_name = emp_name_result[0]

                # Count status types
                count_query = text("SELECT Status, COUNT(*) FROM attendance WHERE EmpNo = :emp_id GROUP BY Status")
                counts = dict(db.session.execute(count_query, {'emp_id': emp_id}).fetchall())

                # Get recent attendance records
                recent_query = text("SELECT Date, Status FROM attendance WHERE EmpNo = :emp_id ORDER BY Date DESC LIMIT 10")
                recent_rows = db.session.execute(recent_query, {'emp_id': emp_id}).fetchall()

                attendance = {
                    'employee_id': emp_id,
                    'employee_name': employee_name,
                    'present_days': counts.get('Present', 0),
                    'absent_days': counts.get('Absent', 0),
                    'late_days': counts.get('Late', 0),
                    'leave_days': counts.get('Leave', 0),
                    'recent_records': [{
                        'date': row[0].strftime('%Y-%m-%d'),
                        'status': row[1].lower(),
                        'check_in': '09:00' if row[1].lower() == 'present' else '--',
                        'check_out': '05:00' if row[1].lower() == 'present' else '--',
                        'working_hours': '08' if row[1].lower() == 'present' else '--'
                    } for row in recent_rows]
                }

        except Exception as e:
            print("Error fetching attendance data:", e)

    return render_template('attendance.html', attendance=attendance)

@app.route('/salary', methods=['GET', 'POST'])
def salary():
    salary_data = None
    searched = False

    if request.method == 'POST':
        emp_id = request.form['employee_id']
        searched = True

        try:
            # Fetch employee name
            emp_name_query = text("SELECT name FROM employee WHERE EmpNo = :emp_id")
            emp_name_result = db.session.execute(emp_name_query, {'emp_id': emp_id}).fetchone()

            # Fetch salary details
            salary_query = text("SELECT SalaryType, FixedSalary, PerDayRate FROM salary WHERE EmpNo = :emp_id")
            salary_result = db.session.execute(salary_query, {'emp_id': emp_id}).fetchone()

            if emp_name_result and salary_result:
                salary_type = salary_result[0]
                fixed_salary = salary_result[1]
                per_day_rate = salary_result[2]

                salary_data = {
                    'Empname': emp_name_result[0],
                    'EmpNo': emp_id,
                    'salarytype': salary_type,
                    'bonus': 0,
                    'allowances': 0,
                    'deductions': 0
                }

                if salary_type == 'Fixed':
                    base_salary = fixed_salary or 0
                    salary_data['base_salary'] = base_salary
                    salary_data['net_salary'] = base_salary
                elif salary_type == 'PerDay':
                    salary_data['per_day_rate'] = per_day_rate or 0
                    salary_data['net_salary'] = 0  # Net salary not for PerDay
                else:
                    salary_data['net_salary'] = 0

        except Exception as e:
            print("Error fetching salary data:", e)

    return render_template('salary.html', salary=salary_data, searched=searched)


@app.route('/salary_history', methods=['GET', 'POST'])
def salary_history():
    salary_data = None
    searched = False

    if request.method == 'POST':
        emp_id = request.form['emp-id']
        searched = True

        try:
            # Get employee name
            emp_name_query = text("SELECT name FROM employee WHERE EmpNo = :emp_id")
            emp_name_result = db.session.execute(emp_name_query, {'emp_id': emp_id}).fetchone()

            # Get full salary history
            history_query = text("SELECT historyid, empno, totalsalary, monthyear FROM salary_history WHERE empno = :emp_id ORDER BY monthyear ASC")
            history_results = db.session.execute(history_query, {'emp_id': emp_id}).fetchall()

            if emp_name_result and history_results:
                emp_name = emp_name_result[0]
                salary_data = {
                    'Empname': emp_name,
                    'empno': emp_id,
                    'history': []
                }

                # Sorting and formatting
                previous_amount = None
                for row in history_results:
                    amount = row[2]
                    if previous_amount is None:
                        change = 0  
                    else: 
                        change= amount - previous_amount
                    salary_data['history'].append({
                        'historyid': row[0],
                        'amount': amount,
                        'date': row[3],
                        'change': change,
                        'change_formatted': f"{'+' if change >= 0 else ''}{change}",
                        'reason': 'Performance Review',  
                        'percentage': min(100, int(amount / 100 ))  # Scale bar height roughly
                    })
                    previous_amount = amount

        except Exception as e:
            print("Error fetching salary history data:", e)

    return render_template('salary_history.html', salary_history=salary_data, searched=searched)

@app.route('/department', methods=['GET', 'POST'])
def department():
    department_data = None
    searched = False

    if request.method == 'POST':
        dept_name = request.form['dept-name']
        searched = True

        try:
            # Fetch department info
            dept_query = text("SELECT Deptid, name, area FROM department WHERE name = :dept_name")
            dept_result = db.session.execute(dept_query, {'dept_name': dept_name}).fetchone()

            if dept_result:
                dept_id = dept_result[0]
                department_data = {
                    'DeptId': dept_result[0],
                    'name': dept_result[1],
                    'area': dept_result[2],
                    'employees': []
                }

                # Fetching  employees
                emp_query = text("SELECT Empno,name FROM employee WHERE Department_ID = :dept_id")
                emp_results = db.session.execute(emp_query, {'dept_id': dept_id}).fetchall()

                for emp in emp_results:
                    department_data['employees'].append({
                        'empno': emp[0],
                        'name': emp[1]
                    })

        except Exception as e:
            print("Error fetching department data:", e)

    return render_template('department.html', department=department_data, searched=searched)

#admin panel work
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        admin_password = request.form['password']

        query = text('SELECT mail, password FROM admin WHERE mail = :mail')
        result = db.session.execute(query, {'mail': admin_id}).fetchone()

        if result:
            db_mail = result[0]
            db_password = result[1]

            if admin_id == db_mail and admin_password == db_password:
                session['admin_logged_in'] = True
                return redirect(url_for('admin_panel'))
            else:
                return render_template('admin_login.html', error='Invalid credentials')
        else:
            return render_template('admin_login.html', error='Admin ID not found')

    return render_template('admin_login.html')

@app.route('/admin_panel')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_panel.html' ,admin_logged_in=True)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        department_id = request.form['department_id']
        manager_id = request.form['manager_id']

        if not all([name, address, phone, department_id, manager_id]):
            return render_template('add_employee.html', error='All fields are required.')

        try:
            # what this 1 do : It checks: "Is there any department in the database with this DeptID?"
            #    If yes → it returns something like (1,) → .first() gives you a result.
            # If no → it returns None.

            dept_exists = db.session.execute(
                text("SELECT 1 FROM department WHERE DeptID = :dept_id"),
                {'dept_id': department_id}
            ).first()
            manager_exists = db.session.execute(
                text("SELECT 1 FROM employee WHERE EmpNo = :mgr_id"),
                {'mgr_id': manager_id}
            ).first()

            if not dept_exists:
                return render_template('add_employee.html', error='Invalid Department ID.')
            if not manager_exists:
                return render_template('add_employee.html', error='Invalid Manager ID.')

            insert_query = text('''
                INSERT INTO employee (name, address, phone_number, department_id, manager_id)
                VALUES (:name, :address, :phone, :department_id, :manager_id)
            ''')

            db.session.execute(insert_query, {
                'name': name,
                'address': address,
                'phone': phone,
                'department_id': department_id,
                'manager_id': manager_id
            })
            db.session.commit()

            return render_template('add_employee.html', success='Employee added successfully.')

        except Exception as e:
            #rollback cancel insertion if any error occurs
            db.session.rollback() 
            return render_template('add_employee.html', error=f"Error: {str(e)}")

    return render_template('add_employee.html')


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        name = request.form['name']
        area = request.form['area']

        if not all([name, area]):
            return render_template('add_department.html', error='All fields are required.')

        try:
            insert_query = text('''
                INSERT INTO department (name, area)
                VALUES (:name, :area)
            ''')

            db.session.execute(insert_query, {
                'name': name,
                'area': area
            })
            db.session.commit()

            return render_template('add_department.html', success='Department added successfully.')

        except Exception as e:
            db.session.rollback()
            return render_template('add_department.html', error=f"Error: {str(e)}")

    return render_template('add_department.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))



if __name__ == '__main__':
    app.run(debug=True)
    