class ClubsManagement:

    def __init__(self, db):
        self.db = db
        self.cursor = db.connection.cursor()

    def add_club(self, club_name, description, contact_person, contact_email):
        user_permission = self.db.users_manager.get_user_permission(self.db.users_manager.current_permission)

        if user_permission and user_permission.lower() == "admin":
            statement = """
                INSERT INTO clubs (club_name, description, contact_person, contact_email)
                VALUES (:club_name, :description, :contact_person, :contact_email)
            """
            self.cursor.execute(statement, club_name=club_name, description=description, contact_person=contact_person, contact_email=contact_email)
            self.db.connection.commit()
            print(f"동아리 '{club_name}'가 추가되었습니다.")
        else:
            print(f"관리자 권한이 없어 동아리를 추가할 수 없습니다. 사용자 권한: {user_permission}")

    def list_applicants_by_club(self, club_name):
        statement = """
            SELECT m.name, a.student_id, a.fiveme, a.content, a.club_name
            FROM applications a
            JOIN members m ON a.student_id = m.student_id
            WHERE a.club_name = :club_name
        """
        self.cursor.execute(statement, club_name=club_name)
        results = self.cursor.fetchall()

        if results:
            print(f"{club_name}에 대한 지원자 현황:")
            for result in results:
                print(f"이름: {result[0]}, 학번: {result[1]}, 5단어: {result[2]}, 동기: {result[3]}")
        else:
            print(f"해당 동아리 '{club_name}'에 대한 지원 현황이 없습니다.")



    # ... 기타 메소드들 ...

    def close(self):
        self.cursor.close()
