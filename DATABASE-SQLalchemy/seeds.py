import random
from faker import Faker
from connect_db import session
from models import Groups, Students, Lectors, Subjects, Marks


fake = Faker()


for i in range(1, 4):
    group = Groups(name=f"Group {i}")
    session.add(group)


for _ in range(50):
    group_id = random.randint(1, 3)
    student = Students(name=fake.name(), group_id=group_id)
    session.add(student)


for _ in range(5):
    lector = Lectors(name=fake.name())
    session.add(lector)


subject_names = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "History",
    "Literature",
    "Computer Science",
]

for name in subject_names:
    lector_id = random.randint(1, 5)
    subject = Subjects(name=name, lector_id=lector_id)
    session.add(subject)


session.commit()


subjects = session.query(Subjects).all()


for student_id in range(1, 51):
    for subject in subjects:
        value = random.randint(1, 100)
        timestamp = fake.date_time_between(start_date="-1y", end_date="now")
        mark = Marks(value=value, timestamp=timestamp, subject_id=subject.id, student_id=student_id)
        session.add(mark)


session.commit()


session.close()