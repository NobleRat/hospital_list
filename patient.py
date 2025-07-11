class Patient:
    def __init__(self, id, first_name, last_name, age, diagnosis, cost):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.diagnosis = diagnosis
        self.cost = cost

    def as_tuple(self):
        return (self.first_name, self.last_name, self.age, self.diagnosis, self.cost)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.age}წ) - {self.diagnosis} - ₾{self.cost}"
