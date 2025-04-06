from faker import Faker
from typing import List
from app.models import Discussion
fake = Faker()

def generate_user(nbr_user: int) -> List[dict]:
    users = []
    for _ in range(nbr_user):
        users.append({
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "userName": fake.user_name(),
            "password": fake.password(length=12),
            "userType": 0
        })
    return users

discussions: List[Discussion] = [
    Discussion(
        id=1,
        d_Name="Data Warehousing & ETL",
        d_Description="Data Warehousing & ETL",
        d_Profile="uploads/8331deec-070b-4515-b401-11f9f1b31cd2.jpg",
        OwnerId="1"
    ),
    Discussion(
        id=2,
        d_Name="Spring Framework (Java)",
        d_Description="Spring Framework (Java)",
        d_Profile="uploads/ab898ba3-3e89-4ae7-9b73-8d50e843d3cc.png",
        OwnerId="1"
    ),
    Discussion(
        id=3,
        d_Name="DevOps & Continuous Integration",
        d_Description="DevOps & Continuous Integration",
        d_Profile="uploads/a92ef780-2ff3-49be-90a2-4ec4d7c4603f.png",
        OwnerId="1"
    ),
    Discussion(
        id=4,
        d_Name="Cybersecurity & Ethical Hacking",
        d_Description="Cybersecurity & Ethical Hacking",
        d_Profile="uploads/431dcfe5-f47a-432e-a236-047bc01171c9.jpg",
        OwnerId="1"
    ),
    Discussion(
        id=5,
        d_Name="Database Administration (Oracle & SQL)",
        d_Description="Database Administration (Oracle & SQL)",
        d_Profile="uploads/eb7e15fb-059f-4a32-a3a4-9f0e0f86bdee.png",
        OwnerId="1"
    ),
    Discussion(
        id=6,
        d_Name="Big Data & Machine Learning",
        d_Description="Big Data & Machine Learning",
        d_Profile="uploads/1b0a46a9-e28e-47a8-84c2-ea8ee2d4fb0b.jpg",
        OwnerId="1"
    ),
    Discussion(
        id=7,
        d_Name="System & Network Administration",
        d_Description="System & Network Administration",
        d_Profile="uploads/6da3e576-5f94-49cf-bbca-d0c222c2e786.jpg",
        OwnerId="1"
    ),
    Discussion(
        id=8,
        d_Name="Software Engineering & Design Patterns",
        d_Description="Software Engineering & Design Patterns",
        d_Profile="uploads/d9f8c893-5810-4193-b927-4b8d09ff00f8.png",
        OwnerId="1"
    ),
    Discussion(
        id=9,
        d_Name="Web & Mobile Development",
        d_Description="Web & Mobile Development",
        d_Profile="uploads/adc96ef8-8f19-4c5a-88b6-664c8a687077.jpg",
        OwnerId="1"
    ),
    Discussion(
        id=10,
        d_Name="Cloud Computing (AWS, Azure, GCP)",
        d_Description="Cloud Computing (AWS, Azure, GCP)",
        d_Profile="uploads/d368b2fd-3c57-45cc-ac16-e1aa69aa9178.jpg",
        OwnerId="1"
    ),
    Discussion(
        id=11,
        d_Name="AI & Machine Learning",
        d_Description="AI & Machine Learning",
        d_Profile="uploads/eb8b9228-b298-4225-b3c6-03e5bfd119f7.png",
        OwnerId="1"
    ),
    Discussion(
        id=12,
        d_Name="Agile Methodologies & Scrum",
        d_Description="Agile Methodologies & Scrum",
        d_Profile="uploads/c0dece46-aacd-4fdb-bb4f-2547310a105d.png",
        OwnerId="1"
    ),
]



