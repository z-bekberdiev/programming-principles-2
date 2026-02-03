class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def total_salary(self):
        return self.base_salary
    
class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent

    def total_salary(self):
        return self.base_salary * (1 + self.bonus_percent / 100)
    
class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects

    def total_salary(self):
        return self.base_salary + self.completed_projects * 500
    
class Intern(Employee):
    def __init__(self, name, base_salary):
        super().__init__(name, base_salary)

    def total_salary(self):
        return super().total_salary()
    
string = input().split()

match string[0]:
    case "Manager":
        manager = Manager(string[1], int(string[2]), int(string[3]))
        print(f"Name: {manager.name}, Total: {manager.total_salary():.2f}")

    case "Developer":
        developer = Developer(string[1], int(string[2]), int(string[3]))
        print(f"Name: {developer.name}, Total: {developer.total_salary():.2f}")
        
    case "Intern":
        intern = Intern(string[1], int(string[2]))
        print(f"Name: {intern.name}, Total: {intern.total_salary():.2f}")