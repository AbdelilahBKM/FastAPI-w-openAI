from faker import Faker

fake = Faker()

class Discussion:
    def __init__(self, id, name):
        self.id = id
        self.name = name

discussions = [
    Discussion(id=1, name="Data Warehousing & ETL"),
    Discussion(id=2, name="Spring Framework (Java)"),
    Discussion(id=3, name="DevOps & Continuous Integration"),
    Discussion(id=4, name="Cybersecurity & Ethical Hacking"),
    Discussion(id=5, name="Database Administration (Oracle & SQL)"),
    Discussion(id=6, name="Big Data & Machine Learning"),
    Discussion(id=7, name="System & Network Administration"),
    Discussion(id=8, name="Software Engineering & Design Patterns"),
    Discussion(id=9, name="Web & Mobile Development"),
    Discussion(id=10, name="Cloud Computing (AWS, Azure, GCP)"),
    Discussion(id=11, name="AI & Machine Learning"),
    Discussion(id=12, name="Agile Methodologies & Scrum")
]

def generate_user(nbr_user):
    users = []
    for _ in range(nbr_user):
        users.append({
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "userName": fake.user_name(),
            "password": fake.password(length=12)
        })
    return users

