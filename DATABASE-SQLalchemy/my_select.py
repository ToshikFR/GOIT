from connect_db import session
from models import Groups, Students, Lectors, Subjects, Marks
from sqlalchemy import func, desc

def main():
    while True:
        select = input("\n Make your choice:")
        if select == '1':
            print(session.query( Students.name, func.round(func.avg(Marks.value), 1).label('avg_mark'))\
            .select_from(Marks).join(Students).group_by(Students.id).order_by(desc('avg_mark')).limit(5).all())
            return
        if select == '2':
            subject_id = session.query(Subjects.id).filter(Subjects.name == 'Mathematics').scalar()
            print(session.query(Students.name, func.round(func.max(Marks.value), 1).label('max_avg_mark')).join(
            Marks, Students.id == Marks.student_id).filter(Marks.subject_id == subject_id).group_by(Students.id, Students.name).order_by(
            func.max(Marks.value).desc()).limit(1).all())
            return 
        if select == '3':
            subject_id = session.query(Subjects.id).filter(Subjects.name == 'Physics').scalar()
            print(session.query(Groups.name, func.round(func.avg(Marks.value), 1).label('avg_mark')).select_from(Groups).join(
            Students).join(Marks).filter(Marks.subject_id == subject_id).group_by(Groups.name).all())
            return 
        if select == '4':
            print(session.query(func.round(func.avg(Marks.value), 1).label('avg_mark')).all())
            return 
        if select == '5':
            lector = session.query(Lectors.id).filter(Lectors.name == 'Brian Parker').scalar()
            print(session.query(Subjects.name).join(Lectors).filter(Lectors.id == lector).group_by(Subjects.name).all())
            return
        if select == '6':
            group = session.query(Groups.id).filter(Groups.name == 'Group 1').scalar()
            print(session.query(Students.name).join(Groups).filter(Groups.id == group).all())
            return
        if select == '7':
            group = session.query(Groups.id).filter(Groups.name == 'Group 1').scalar()
            subject = session.query(Subjects.id).filter(Subjects.name == 'Physics').scalar()
            print(session.query(Students.name, Marks.value).join(Marks, Students.id == Marks.student_id
            ).filter(Students.group_id == group, Marks.subject_id == subject).all())
            return
        if select == '8':
            lector = session.query(Lectors.id).filter(Lectors.name == 'Brian Parker')
            print(session.query(Lectors.name, func.round(func.avg(Marks.value), 1).label('avg mark'))
            .join(Subjects, Subjects.id == Marks.subject_id).filter(Lectors.id == lector).all())
            return
        if select == '9':
            student= session.query(Students.id).filter(Students.name == 'Jesse Palmer').scalar()
            print(session.query(Subjects.name).join(Marks, Marks.subject_id == Subjects.id)
            .filter(Marks.student_id == student). distinct().all())
            return
        if select == '10':
            student = session.query(Students.id).filter(Students.name == 'Jesse Palmer').scalar()
            lector = session.query(Lectors.id).filter(Lectors.name == 'Brian Parker').scalar()
            print(session.query(Subjects.name)
            .filter(Marks.student_id == student, Marks.subject_id == Subjects.id, Subjects.lector_id == lector).all())
            return


if __name__ == "__main__":
    main()