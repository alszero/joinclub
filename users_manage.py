class UsersManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.current_user_id = None  # 현재 로그인한 사용자의 학번을 저장하는 변수

    def register_user(self, name, student_id, email, password, tel, permission):
        cursor = self.db_connection.cursor
        statement = """
            INSERT INTO members (member_id, name, student_id, email, password, tel, permission)
            VALUES (member_id_seq.NEXTVAL, :name, :student_id, :email, :password, :tel, :permission)
        """
        cursor.execute(statement, name=name, student_id=student_id, email=email, password=password, tel=tel, permission=permission)
        self.db_connection.connection.commit()
        print("회원가입 완료")

    def get_user_permission(self, user_id):
        cursor = self.db_connection.cursor
        statement = "SELECT permission FROM members WHERE student_id = :user_id"
        cursor.execute(statement, user_id=user_id)
        permission = cursor.fetchone()
        return permission[0] if permission else None
    
    def get_user_name(self, student_id):
        cursor = self.db_connection.cursor
        statement = "SELECT name FROM members WHERE student_id = :student_id"
        cursor.execute(statement, student_id=student_id)
        name = cursor.fetchone()
        return name[0] if name else None

    def login(self, email, password):
        cursor = self.db_connection.cursor
        statement = """
            SELECT student_id, name FROM members
            WHERE email = :email AND password = :password
        """
        cursor.execute(statement, email=email, password=password)
        row = cursor.fetchone()
        if row:
            self.current_user_id = row[0]  # 로그인 성공 시 current_user_id 설정
            return row[1]  # 로그인한 사용자 이름 반환
        else:
            print("로그인 실패")
            return None
