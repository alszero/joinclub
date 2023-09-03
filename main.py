from users_manage import UsersManager
from db import DBconfig
from applications import ApplicationsManagement
from clubs import ClubsManagement

def main():
    db = DBconfig("administrator", "2023", "localhost", "1521", "XE")
    users_manager = UsersManager(db)
    applicants_system = ApplicationsManagement(db)
    clubs_manager = ClubsManagement(db)  # ClubsManagement 인스턴스 생성

    logged_in = False  # 사용자 로그인 상태를 나타내는 변수

    while True:
        print("| ===== 동아리 지원 시스템 ===== |")
        print("|       1. 회원가입              |")
        if not logged_in:
            print("|       2. 로그인                |")
        else: 
            print("|       3. 동아리지원서 작성     |")
            print("|       4. 나의 동아리 지원 현황 |")
            print("|       5. 동아리 추가           |")
            print("|       6. 동아리 지원 현황 조회 |")
            print("|       7. 지원서 수정           |")  # 메뉴에 지원서 수정 메뉴 추가
            print("|       8. 지원서 삭제           |")  # 메뉴에 지원서 삭제 메뉴 추가
        print("|       9. 종료                  |")
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

        elif choice == "2" and not logged_in:
            email = input("이메일: ")
            password = input("비밀번호: ")

            user_name, user_permission = users_manager.login(email, password)
            if user_name:
                print()
                print(f"로그인 성공! 이름: {user_name}님 환영합니다.")
                print(f"사용자 이름: {user_name}, 사용자 권한: {user_permission}")
                print()
                logged_in = True
            else:
                print()
                print("로그인 실패")
                print()

        elif choice == "3" and logged_in:
            user_id = users_manager.current_user_id  # 현재 로그인한 사용자의 학번을 가져옴
            user_name = users_manager.get_user_name(user_id)  # 현재 로그인한 사용자의 이름을 가져옴
            five_me = input("5단어로 나를 표현해주세요: ")
            content = input("동아리 지원 동기: ")
            club_name = input("동아리 이름: ")

            applicants_system.apply_for_club(user_id, user_name, five_me, content, club_name)
            print("동아리 지원서가 제출되었습니다.")

            
        elif choice == "4" and logged_in:
            # 지원 현황 조회
            applicants_system.list_applicants()

        elif choice == "5" and logged_in:
            user_permission = users_manager.get_user_permission(users_manager.current_user_id)
            if user_permission == "admin":
                club_name = input("동아리 이름: ")
                description = input("동아리 설명: ")
                contact_person = input("담당자 이름: ")
                contact_email = input("담당자 이메일: ")

                clubs_manager.add_club(club_name, description, contact_person, contact_email)
            else:
                print()
                print("관리자만 동아리를 추가할 수 있습니다.")
                print()

        elif choice == "6" and logged_in:
            # 관리자인 경우에만 동아리별 지원 현황 조회 기능 수행
            user_permission = users_manager.get_user_permission(users_manager.current_user_id)
            if user_permission == "admin":
                club_name = input("동아리 이름: ")
                clubs_manager.list_applicants_by_club(club_name)
            else:
                print("관리자만 동아리별 지원 현황 조회를 할 수 있습니다.")

        elif choice == "7" and logged_in:
            student_id = input("학번을 입력하세요: ")
            club_name = input("동아리 이름을 입력하세요: ")
            five_me = input("수정할 5단어를 입력하세요: ")
            content = input("수정할 지원 동기를 입력하세요: ")
            
            # 학번과 동아리 이름을 이용하여 지원서 수정
            applicants_system.update_application(student_id, club_name, five_me, content)

        elif choice == "8" and logged_in:
            student_id = input("학번을 입력하세요: ")
            club_name = input("동아리 이름을 입력하세요: ")

            # 학번과 동아리 이름을 이용하여 지원서 삭제
            applicants_system.delete_application(student_id, club_name)
            print("지원서가 삭제되었습니다.")

        elif choice == "9":
            db.exit()
            users_manager.logout_and_exit()
            break

if __name__ == "__main__":
    main()
