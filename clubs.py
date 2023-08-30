class ClubsManagement:

    def __init__(self, db):
        self.db = db
        self.cursor = db.connection.cursor()

    def add_club(self, club_name, description, contact_person, contact_email):
        user_permission = self.db.users_manager.get_user_permission(self.db.users_manager.current_user_id)
        if user_permission == "admin":
            statement = """
                INSERT INTO clubs (club_name, description, contact_person, contact_email)
                VALUES (:club_name, :description, :contact_person, :contact_email)
            """
            self.cursor.execute(statement, club_name=club_name, description=description, contact_person=contact_person, contact_email=contact_email)
            self.db.connection.commit()
            print(f"동아리 '{club_name}'가 추가되었습니다.")
        else:
            print("관리자 권한이 없어 동아리를 추가할 수 없습니다.")

    


    def list_applicants_by_club(self, club_name):
        statement = """
            SELECT a.club_name, COUNT(a.student_id) AS applicant_count
            FROM applications a
            WHERE a.club_name = :club_name
            GROUP BY a.club_name
        """
        self.cursor.execute(statement, club_name=club_name)
        result = self.cursor.fetchone()

        if result:
            print(f"동아리 이름: {result[0]}, 지원자 수: {result[1]}")
        else:
            print("해당 동아리에 대한 지원 현황이 없습니다.")


    # ... 기타 메소드들 ...

    def close(self):
        self.cursor.close()
