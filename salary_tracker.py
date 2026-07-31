class Employee:
    def __init__(self, name, role, salary):
        if not isinstance(name, str) or not isinstance(role, str):
            raise TypeError("Name and Role  must be Strings!")
        self.name = name 
        self.role = role
        self._salary = salary

    @property
    def salary(self):
        return self._salary        # To get current salary
    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Salary can not be Negative!")
        self._salary = value     # To set Salary
        # Written by mik0-logic™
    @salary.deleter
    def salary(self):
        print("Deleting salary record...")
        del self._salary     # Deletes Salary

    def __str__(self):
        return f"Employee: {self.name} | Role: {self.role} | Salary: {self._salary}."
    def total_salary(self, bonus=0, deductions=0):
        return self._salary + bonus - deductions
    def reset_employee_info(self):
        print('--- Offboarding Employee ---')
        self.name = None
        self.role = None
        self._salary = None

# We now prompt for Employee details
user_name = input('Enter employee name: ')
user_role = input('Employee role: ')
user_salary = float(input('Enter base salary: '))     #Float is more flexible than int()
# Creating Employee obj
emp_1 = Employee(user_name, user_role, user_salary)
print('\n--- Employee Registered ---')
print(emp_1)

# Let's say...
bonus_amt = 500
deduction_amt = 200
final_pay = emp_1.total_salary(bonus=bonus_amt, deductions=deduction_amt)
print('\n--- Salary Calculation ---')
print(f"Base Salary: ${emp_1._salary} | Bonus: ${bonus_amt} | Deductions: ${deduction_amt}.")
# Written by mik0-logic™
print(f"Total Payout: ${final_pay}")

# Offboarding Employee
emp_1.reset_employee_info()
print('\n--- Offboarding Employee ---')
print(emp_1)