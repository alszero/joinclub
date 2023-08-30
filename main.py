from users_manage import UsersManager
from db import DBconfig
from applications import ApplicationsManagement
from clubs import ClubsManagement

def main():
    db = DBconfig("administrator", "2023", "localhost", "1521", "XE")
    users_manager = UsersManager(db)
    applicants_system = ApplicationsManagement(db)
    clubs_manager = ClubsManagement(db)  # ClubsManagement 인스턴스 생성
    

    while True:
        print("| ===== 동아리 지원 시스템 ===== |")
        print("|       1. 회원가입              |")
        print("|       2. 로그인                |") 
        print("|       3. 동아리지원서 작성     |")
        print("|       4. 나의 동아리 지원 현황 |")
        print("|       5. 동아리 추가           |")
        print("|       6. 동아리 지원 현황 조회 |")
        print("|       7. 종료                  |")
        print("|================================|")

        choice = input("원하는 작업 선택: ")
        
        if choice == "1":
            name = input("사용자 이름: ")
            student_id = input("학번: ")
            email = input("이메일: ")
            password = input("비밀번호: ")
            tel = input("전화번호: ")
            permission = input("권한(admin/user): ")

            users_manager.register_user(name, student_id, email, password, tel, permission)
            print("회원가입이 완료되었습니다.")

        elif choice == "2":
            email = input("이메일: ")
            password = input("비밀번호: ")

            user_name = users_manager.login(email, password)
            if user_name:
                print()
                print(f"로그인 성공! 이름: {user_name}님 환영합니다.")
                print()
            else:
                print()
                print("로그인 실패")
                print()

        elif choice == "3":
            user_id = users_manager.current_user_id  # 현재 로그인한 사용자의 학번을 가져옴
            user_name = users_manager.get_user_name(user_id)  # 현재 로그인한 사용자의 이름을 가져옴
            five_me = input("5단어로 나를 표현해주세요: ")
            content = input("동아리 지원 동기: ")
            club_name = input("동아리 이름: ")

            applicants_system.apply_for_club(user_id, user_name, five_me, content, club_name)
            print("동아리 지원서가 제출되었습니다.")

            
        elif choice == "4":
            # 지원 현황 조회
            applicants_system.list_applicants()

        elif choice == "5":
            user_permission = users_manager.get_user_permission(users_manager.current_user_id)
            if user_permission == "admin":
                club_name = input("동아리 이름: ")
                description = input("동아리 설명: ")
                contact_person = input("담당자 이름: ")
                contact_email = input("담당자 이메일: ")

                clubs_manager.add_club(club_name, description, contact_person, contact_email)
            else:
                print()
                print("로그인 후 이용해주세요.")
                print()
        elif choice == "6":
            # 관리자인 경우에만 동아리별 지원 현황 조회 기능 수행
            user_permission = users_manager.get_user_permission(users_manager.current_user_id)
            if user_permission == "admin":
                club_name = input("동아리 이름: ")
                clubs_manager.list_applicants_by_club(club_name)
            else:
                print("관리자만 동아리별 지원 현황 조회를 할 수 있습니다.")

        elif choice == "7":
            db.exit()
            break

if __name__ == "__main__":
    main()
