import streamlit as st
import pandas as pd
import sqlite3

# Create connection to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create tables and insert data
cursor.execute('''
    CREATE TABLE Bonus (
        employee_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        Bonus INTEGER
    );
''')
cursor.execute('''
    INSERT INTO Bonus (employee_id, first_name, last_name, bonus) VALUES
    (1, 'John', 'Doe', 6000),
    (2, 'Jane', 'Smith', 5000),
    (3, 'Michael', 'Johnson', 5500),
    (4, 'Michael', 'Johnson', NULL);
''')

cursor.execute('''
    CREATE TABLE employees (
        employee_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone_number TEXT,
        hire_date DATE,
        job_id TEXT,
        salary DECIMAL(10, 2),
        department_id INTEGER
    );
''')
cursor.execute('''
    INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES
    (1, 'John', 'Doe', 'john.doe@example.com', '555-1234', '2022-01-15', 'IT_PROG', 60000.00, 10),
    (2, 'Jane', 'Smith', 'jane.smith@example.com', '555-5678', '2021-03-12', 'HR_REP', 50000.00, 20),
    (3, 'Michael', 'Johnson', 'michael.johnson@example.com', '555-8765', '2020-07-01', 'FIN_ANAL', 55000.00, 30),
    (4, 'Emily', 'Davis', 'emily.davis@example.com', '555-2345', '2019-11-21', 'IT_PROG', 62000.00, 10),
    (5, 'David', 'Wilson', 'david.wilson@example.com', '555-3456', '2018-09-15', 'HR_MGR', 70000.00, 20),
    (6, 'Sarah', 'Brown', 'sarah.brown@example.com', '555-4567', '2023-02-01', 'FIN_ANAL', 56000.00, 30),
    (7, 'James', 'Jones', 'james.jones@example.com', '555-5678', '2021-12-31', 'IT_PROG', 59000.00, 10),
    (8, 'Patricia', 'Garcia', 'patricia.garcia@example.com', '555-6789', '2020-05-20', 'HR_REP', 48000.00, 20),
    (9, 'Robert', 'Martinez', 'robert.martinez@example.com', '555-7890', '2022-08-14', 'FIN_MGR', 75000.00, 30),
    (10, 'Linda', 'Anderson', 'linda.anderson@example.com', '555-8901', '2019-06-30', 'IT_PROG', 61000.00, 10);
''')

conn.commit()

# Define SQL practice questions
questions = [
    {
        "question": "Write a query to find the first and last names of employees who have received a bonus but earn less than the average salary of all employees.",
        "hint": "Use a JOIN between the employees and Bonus tables, and compare the salary with the result of a subquery for the average salary.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.salary < (SELECT AVG(salary) FROM employees);"
    },
    {
        "question": "Write a query to find the employees who do not have a bonus but have a salary greater than 60,000.",
        "hint": "Use a LEFT JOIN and filter for NULL values in the Bonus table.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e LEFT JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus IS NULL AND e.salary > 60000;"
    },
    {
        "question": "Write a query to calculate the total bonus awarded to employees in the HR department.",
        "hint": "Use a JOIN between the employees and Bonus tables, and filter by department_id.",
        "solution": "SELECT SUM(b.Bonus) FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.department_id = 20;"
    },
    {
        "question": "Write a query to find the names of employees who share the same first and last name but work in different departments.",
        "hint": "Use a self-join on the employees table and compare department IDs.",
        "solution": "SELECT e1.first_name, e1.last_name FROM employees e1 JOIN employees e2 ON e1.first_name = e2.first_name AND e1.last_name = e2.last_name WHERE e1.department_id <> e2.department_id;"
    },
    {
        "question": "Write a query to list the names of employees who have been working for more than 3 years in the company and have received a bonus.",
        "hint": "Use the DATE() function to calculate the difference between the hire_date and the current date, and join with the Bonus table.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE (strftime('%Y', 'now') - strftime('%Y', e.hire_date)) > 3;"
    },
    {
        "question": "Write a query to find the department with the highest average salary.",
        "hint": "Group by department_id and use the AVG() function to calculate the average salary.",
        "solution": "SELECT department_id FROM employees GROUP BY department_id ORDER BY AVG(salary) DESC LIMIT 1;"
    },
    {
        "question": "Write a query to find the employee with the longest tenure in the company.",
        "hint": "Use the MIN() function on the hire_date column.",
        "solution": "SELECT first_name, last_name FROM employees WHERE hire_date = (SELECT MIN(hire_date) FROM employees);"
    },
    {
        "question": "Write a query to find the total salary expense of the IT department.",
        "hint": "Sum the salaries of all employees where department_id is 10.",
        "solution": "SELECT SUM(salary) FROM employees WHERE department_id = 10;"
    },
    {
        "question": "Write a query to find the email addresses of employees who received the second-highest bonus.",
        "hint": "Use a subquery to find the second-highest bonus and then filter the Bonus table.",
        "solution": "SELECT e.email FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus = (SELECT MAX(Bonus) FROM Bonus WHERE Bonus < (SELECT MAX(Bonus) FROM Bonus));"
    },
    {
        "question": "Write a query to find all employees who have the same job_id as John Doe.",
        "hint": "Use a subquery to find John Doe's job_id.",
        "solution": "SELECT first_name, last_name FROM employees WHERE job_id = (SELECT job_id FROM employees WHERE first_name = 'John' AND last_name = 'Doe');"
    },
    {
        "question": "Write a query to find the employee with the maximum salary in each department.",
        "hint": "Group by department_id and use the MAX() function on the salary column.",
        "solution": "SELECT first_name, last_name, department_id, salary FROM employees WHERE (department_id, salary) IN (SELECT department_id, MAX(salary) FROM employees GROUP BY department_id);"
    },
    {
        "question": "Write a query to find employees who have received a bonus and are working in departments with fewer than 3 employees.",
        "hint": "Use a subquery to count employees in each department and then filter.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.department_id IN (SELECT department_id FROM employees GROUP BY department_id HAVING COUNT(employee_id) < 3);"
    },
    {
        "question": "Write a query to find the total number of employees who have received a bonus in each department.",
        "hint": "Use a JOIN between the employees and Bonus tables and GROUP BY department_id.",
        "solution": "SELECT e.department_id, COUNT(e.employee_id) FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id GROUP BY e.department_id;"
    },
    {
        "question": "Write a query to list the employees who received a bonus greater than the average bonus.",
        "hint": "Use the AVG() function on the Bonus table and filter for bonuses greater than this value.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus > (SELECT AVG(Bonus) FROM Bonus);"
    },
    {
        "question": "Write a query to find the difference in salary between the highest-paid and the lowest-paid employees.",
        "hint": "Use the MAX() and MIN() functions on the salary column.",
        "solution": "SELECT MAX(salary) - MIN(salary) AS salary_difference FROM employees;"
    },
    {
        "question": "Write a query to find employees whose salaries are within 10% of the highest salary.",
        "hint": "Use the MAX() function to find the highest salary, and calculate the 10% range.",
        "solution": "SELECT first_name, last_name FROM employees WHERE salary >= 0.9 * (SELECT MAX(salary) FROM employees);"
    },
    {
        "question": "Write a query to find the employee who received the highest bonus and their corresponding salary.",
        "hint": "Use a JOIN and filter for the maximum bonus.",
        "solution": "SELECT e.first_name, e.last_name, e.salary FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus = (SELECT MAX(Bonus) FROM Bonus);"
    },
    {
        "question": "Write a query to find the total bonus amount awarded to employees hired after January 1, 2022.",
        "hint": "Use a WHERE clause on the hire_date column and JOIN with the Bonus table.",
        "solution": "SELECT SUM(b.Bonus) FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.hire_date > '2022-01-01';"
    },
    {
        "question": "Write a query to list all employees who have the same last name as another employee but a different department.",
        "hint": "Use a self-join on the last_name column and compare department_id.",
        "solution": "SELECT e1.first_name, e1.last_name FROM employees e1 JOIN employees e2 ON e1.last_name = e2.last_name AND e1.department_id <> e2.department_id;"
    },
    {
        "question": "Write a query to find the average salary of employees who have not received a bonus.",
        "hint": "Use a LEFT JOIN and filter for NULL values in the Bonus table.",
        "solution": "SELECT AVG(e.salary) FROM employees e LEFT JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus IS NULL;"
    },
    {
        "question": "Write a query to find employees who are working in departments where the average salary is below 60,000.",
        "hint": "Use a subquery to calculate the average salary per department.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e WHERE e.department_id IN (SELECT department_id FROM employees GROUP BY department_id HAVING AVG(salary) < 60000);"
    },
    {
        "question": "Write a query to list the names of employees who have been hired in the last 2 years and have received a bonus.",
        "hint": "Use the DATE() function to calculate the hire date difference, and JOIN with the Bonus table.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE strftime('%Y', 'now') - strftime('%Y', e.hire_date) <= 2;"
    },
    {
        "question": "Write a query to find employees who work in the same department as the highest-paid employee.",
        "hint": "Use a subquery to find the department_id of the highest-paid employee.",
        "solution": "SELECT first_name, last_name FROM employees WHERE department_id = (SELECT department_id FROM employees WHERE salary = (SELECT MAX(salary) FROM employees));"
    },
    {
        "question": "Write a query to find the email addresses of employees who have a bonus less than the minimum bonus received by any employee in the IT department.",
        "hint": "Use a subquery to find the minimum bonus in the IT department.",
        "solution": "SELECT e.email FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus < (SELECT MIN(b.Bonus) FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.department_id = 10);"
    },
    {
        "question": "Write a query to find the department with the highest total bonus awarded to employees.",
        "hint": "Use a JOIN between the employees and Bonus tables, and GROUP BY department_id.",
        "solution": "SELECT e.department_id FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id GROUP BY e.department_id ORDER BY SUM(b.Bonus) DESC LIMIT 1;"
    },
    {
        "question": "Write a query to list employees who have the same first name as the highest-paid employee but a different last name.",
        "hint": "Use a subquery to find the first name of the highest-paid employee, and filter the results.",
        "solution": "SELECT first_name, last_name FROM employees WHERE first_name = (SELECT first_name FROM employees WHERE salary = (SELECT MAX(salary) FROM employees)) AND last_name <> (SELECT last_name FROM employees WHERE salary = (SELECT MAX(salary) FROM employees));"
    },
    {
        "question": "Write a query to find employees who have received a bonus greater than 10% of their salary.",
        "hint": "Use a JOIN between the employees and Bonus tables, and compare the bonus to 10% of the salary.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus > 0.1 * e.salary;"
    },
    {
        "question": "Write a query to find the total number of employees who were hired in each year and received a bonus.",
        "hint": "Use the strftime() function to extract the year from hire_date and GROUP BY year.",
        "solution": "SELECT strftime('%Y', e.hire_date) AS hire_year, COUNT(e.employee_id) FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id GROUP BY hire_year;"
    },
    {
        "question": "Write a query to find the second highest-paid employee in each department.",
        "hint": "Use a subquery with ROW_NUMBER() or RANK() to find the second highest salary per department.",
        "solution": "SELECT first_name, last_name, department_id, salary FROM (SELECT first_name, last_name, department_id, salary, ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank FROM employees) WHERE salary_rank = 2;"
    },
    {
        "question": "Write a query to find the employee with the highest bonus-to-salary ratio.",
        "hint": "Use a JOIN between the employees and Bonus tables, and calculate the ratio.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id ORDER BY b.Bonus / e.salary DESC LIMIT 1;"
    },
    {
        "question": "Write a query to find the total number of employees who have been working for more than 5 years and have received a bonus.",
        "hint": "Use the DATE() function to calculate the tenure, and JOIN with the Bonus table.",
        "solution": "SELECT COUNT(e.employee_id) FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE (strftime('%Y', 'now') - strftime('%Y', e.hire_date)) > 5;"
    },
    {
        "question": "Write a query to list employees who have the same last name but work in different departments and have received a bonus.",
        "hint": "Use a self-join on the last_name column and filter by department_id and Bonus.",
        "solution": "SELECT e1.first_name, e1.last_name FROM employees e1 JOIN employees e2 ON e1.last_name = e2.last_name AND e1.department_id <> e2.department_id JOIN Bonus b1 ON e1.employee_id = b1.employee_id JOIN Bonus b2 ON e2.employee_id = b2.employee_id;"
    },
    {
        "question": "Write a query to find the email addresses of employees whose salary is below the average salary of their department and have received a bonus.",
        "hint": "Use a subquery to calculate the average salary per department, and JOIN with the Bonus table.",
        "solution": "SELECT e.email FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.salary < (SELECT AVG(salary) FROM employees WHERE department_id = e.department_id);"
    },
    {
        "question": "Write a query to list the first names and last names of employees who have the same job_id as employees who have received the maximum bonus.",
        "hint": "Use a subquery to find the job_id of the employee with the maximum bonus.",
        "solution": "SELECT first_name, last_name FROM employees WHERE job_id = (SELECT job_id FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus = (SELECT MAX(Bonus) FROM Bonus));"
    },
    {
        "question": "Write a query to find employees who have received a bonus and have been working for more than the average tenure of all employees.",
        "hint": "Use a subquery to calculate the average tenure and JOIN with the Bonus table.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE (strftime('%Y', 'now') - strftime('%Y', e.hire_date)) > (SELECT AVG(strftime('%Y', 'now') - strftime('%Y', hire_date)) FROM employees);"
    },
    {
        "question": "Write a query to find the first and last names of employees who have the same first name but a different last name as the employee with the highest bonus.",
        "hint": "Use a subquery to find the first name of the employee with the highest bonus.",
        "solution": "SELECT first_name, last_name FROM employees WHERE first_name = (SELECT first_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus = (SELECT MAX(Bonus) FROM Bonus)) AND last_name <> (SELECT last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus = (SELECT MAX(Bonus) FROM Bonus));"
    },
    {
        "question": "Write a query to find the department with the lowest average salary where all employees have received a bonus.",
        "hint": "Use a GROUP BY and HAVING clause on department_id with a JOIN.",
        "solution": "SELECT department_id FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id GROUP BY e.department_id HAVING AVG(e.salary) = (SELECT MIN(AVG(salary)) FROM employees GROUP BY department_id) AND COUNT(e.employee_id) = (SELECT COUNT(*) FROM employees e1 JOIN Bonus b1 ON e1.employee_id = b1.employee_id WHERE e1.department_id = e.department_id);"
    },
    {
        "question": "Write a query to find employees who have the same job_id as employees who received the lowest salary in their department but still received a bonus.",
        "hint": "Use a subquery to find the job_id of the employee with the lowest salary in each department.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.job_id = (SELECT job_id FROM employees e1 WHERE salary = (SELECT MIN(salary) FROM employees WHERE department_id = e1.department_id));"
    },
    {
        "question": "Write a query to find the first and last names of employees who work in the same department as the employee with the longest tenure and have received a bonus.",
        "hint": "Use a subquery to find the department_id of the employee with the longest tenure.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.department_id = (SELECT department_id FROM employees WHERE hire_date = (SELECT MIN(hire_date) FROM employees));"
    },
    {
        "question": "Write a query to find the average bonus awarded to employees in departments where the highest-paid employee has a salary greater than 70,000.",
        "hint": "Use a subquery to find the departments with the highest-paid employees earning over 70,000.",
        "solution": "SELECT AVG(b.Bonus) FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.department_id IN (SELECT department_id FROM employees GROUP BY department_id HAVING MAX(salary) > 70000);"
    },
    {
        "question": "Write a query to find the first and last names of employees who have been working for less than the average tenure of employees who received a bonus.",
        "hint": "Use a subquery to calculate the average tenure of employees with a bonus.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e WHERE (strftime('%Y', 'now') - strftime('%Y', e.hire_date)) < (SELECT AVG(strftime('%Y', 'now') - strftime('%Y', e1.hire_date)) FROM employees e1 JOIN Bonus b ON e1.employee_id = b.employee_id);"
    },
    {
        "question": "Write a query to find the employee with the most recent hire date who has also received a bonus.",
        "hint": "Use a JOIN and filter for the maximum hire_date.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.hire_date = (SELECT MAX(hire_date) FROM employees);"
    },
    {
        "question": "Write a query to list the first and last names of employees who work in departments with fewer than 5 employees and have received a bonus.",
        "hint": "Use a subquery to count employees in each department and filter for departments with fewer than 5 employees.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.department_id IN (SELECT department_id FROM employees GROUP BY department_id HAVING COUNT(employee_id) < 5);"
    },
    {
        "question": "Write a query to find the average salary of employees who have received the highest bonus in their department.",
        "hint": "Use a subquery to find the employees with the highest bonus per department.",
        "solution": "SELECT AVG(e.salary) FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus = (SELECT MAX(Bonus) FROM Bonus b1 JOIN employees e1 ON b1.employee_id = e1.employee_id WHERE e1.department_id = e.department_id);"
    },
    {
        "question": "Write a query to find the first and last names of employees who have a higher salary than the average salary in their department and have received a bonus.",
        "hint": "Use a subquery to calculate the average salary per department and filter for employees with a higher salary.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.salary > (SELECT AVG(salary) FROM employees WHERE department_id = e.department_id);"
    },
    {
        "question": "Write a query to find employees who have the same last name as the employee with the lowest salary but work in a different department and have received a bonus.",
        "hint": "Use a subquery to find the last name of the employee with the lowest salary.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE e.last_name = (SELECT last_name FROM employees WHERE salary = (SELECT MIN(salary) FROM employees)) AND e.department_id <> (SELECT department_id FROM employees WHERE salary = (SELECT MIN(salary) FROM employees));"
    },
    {
        "question": "Write a query to list the first and last names of employees who have received the same bonus amount as the employee with the highest salary in their department.",
        "hint": "Use a subquery to find the bonus of the highest-paid employee in each department.",
        "solution": "SELECT e.first_name, e.last_name FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id WHERE b.Bonus = (SELECT b1.Bonus FROM employees e1 JOIN Bonus b1 ON e1.employee_id = b1.employee_id WHERE e1.department_id = e.department_id AND e1.salary = (SELECT MAX(salary) FROM employees WHERE department_id = e.department_id));"
    },
    {
        "question": "Write a query to find the department with the most employees who have received a bonus.",
        "hint": "Use a JOIN and GROUP BY department_id, and count the number of employees.",
        "solution": "SELECT e.department_id FROM employees e JOIN Bonus b ON e.employee_id = b.employee_id GROUP BY e.department_id ORDER BY COUNT(e.employee_id) DESC LIMIT 1;"
    }
]


# Initialize session state to keep track of solved questions
if "solved" not in st.session_state:
    st.session_state["solved"] = [False] * len(questions)

def sql_executor(query):
    try:
        result = pd.read_sql_query(query, conn)
        return result
    except Exception as e:
        return str(e)

def main():
    st.title("SQL Practice Application")

    # Display table schemas
    st.header("Table Schemas")
    if st.checkbox("Bonus Table Schema"):
        bonus_schema = pd.read_sql_query("PRAGMA table_info(Bonus);", conn)
        st.write(bonus_schema)
    
    if st.checkbox("Employees Table Schema"):
        employees_schema = pd.read_sql_query("PRAGMA table_info(employees);", conn)
        st.write(employees_schema)
    
    # Select a question
    question_index = st.selectbox(
        "Select a Question", 
        range(len(questions)), 
        format_func=lambda x: f"Question {x+1} {'✔️' if st.session_state['solved'][x] else ''}"
    )
    question = questions[question_index]

    # Display the selected question
    st.write(question["question"])

    # Provide input for the SQL query
    user_query = st.text_area("Write your SQL query here:")

    # Submit button
    if st.button("Run Query"):
        result = sql_executor(user_query)
        st.write(result)

        if result.equals(sql_executor(question["solution"])):
            st.session_state["solved"][question_index] = True
            st.success("Correct, hurrah! ✔️")
        else:
            st.session_state["solved"][question_index] = False
            st.error("Incorrect, try again ❌")

    # Option to view the answer
    if st.button("View Answer"):
        st.write(f"Answer: {question['solution']}")

    

if __name__ == "__main__":
    main()
