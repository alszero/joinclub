from datetime import datetime

class ApplicationsManagement:
    
    def __init__(self, db_connection):
        self.connection = db_connection
        self.cursor = db_connection.get_cursor()

    def apply_for_club(self, student_id, name, five_me, content, club_name):
        apply_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        user_id_query = """
            SELECT member_id FROM members WHERE student_id = :student_id
        """
        self.cursor.execute(user_id_query, student_id=student_id)
        user_id = self.cursor.fetchone()[0]

        statement = """
            INSERT INTO applications (application_id, club_name, student_id, fiveme, content, apply_date, name)
            VALUES (application_id_seq.NEXTVAL, :club_name, :student_id, :five_me, :content, TO_DATE(:apply_date, 'YYYY-MM-DD HH24:MI:SS'), :name)
        """
        self.cursor.execute(statement, club_name=club_name, student_id=student_id, five_me=five_me, content=content, apply_date=apply_date, name=name)
        self.connection.connection.commit()
        print("동아리 지원서가 제출되었습니다.")

        
    def list_applicants(self):
        statement = """
            SELECT m.name, a.student_id, a.fiveme, a.content, a.club_name
            FROM applications a
            JOIN members m ON a.student_id = m.student_id
        """
        self.cursor.execute(statement)
        applicants = self.cursor.fetchall()
        
        if not applicants:
            print("동아리 지원 현황: 동아리에 지원하지 않으셨습니다.")
        else:
            print("동아리 지원 현황:")
            for applicant in applicants:
                print(f"이름: {applicant[0]}, 학번: {applicant[1]}, 5단어: {applicant[2]}, 지원 동기: {applicant[3]}, 동아리 이름: {applicant[4]}")
                

    def update_application(self, student_id, club_name, five_me, content):
        user_id_query = """
            SELECT member_id FROM members WHERE student_id = :student_id
        """
        self.cursor.execute(user_id_query, student_id=student_id)
        user_id = self.cursor.fetchone()[0]

        update_statement = """
            UPDATE applications
            SET fiveme = :five_me, content = :content
            WHERE student_id = :student_id AND club_name = :club_name
        """
        self.cursor.execute(update_statement, student_id=student_id, club_name=club_name, five_me=five_me, content=content)
        self.connection.connection.commit()
        print("지원서가 수정되었습니다.")

    def delete_application(self, student_id, club_name):
        delete_statement = """
            DELETE FROM applications
            WHERE student_id = :student_id AND club_name = :club_name
        """
        self.cursor.execute(delete_statement, student_id=student_id, club_name=club_name)
        self.connection.connection.commit()
    
    def close(self):
        self.cursor.close()
        self.connection.close()
