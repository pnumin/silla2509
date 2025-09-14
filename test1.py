# -*- coding: utf-8 -*-

# 2025년을 기준으로 사용자의 출생 연도와 생일 경과 여부를 입력받아
# '만 나이'를 계산하고 출력하는 프로그램입니다.

BASE_YEAR = 2025

# 1. 사용자로부터 출생 연도 입력받기
# (사용자가 올바른 4자리 숫자를 입력했다고 가정합니다)
birth_year_str = input("출생 연도를 4자리 숫자로 입력하세요 (예: 1995): ")
birth_year = int(birth_year_str)

# 2. 사용자로부터 생일 경과 여부 입력받기
# (사용자가 'y' 또는 'n'을 입력했다고 가정합니다)
birthday_passed_input = input("올해 생일이 지났나요? (지났으면 'y', 지나지 않았으면 'n'): ").lower()

# 3. '만 나이' 계산 (생일이 지나지 않았으면 1을 뺌)
age = BASE_YEAR - birth_year
if birthday_passed_input == 'n':
    age -= 1

# 4. 결과 출력
print(f"\n{BASE_YEAR}년 기준, 당신의 만 나이는 {age}세입니다.")