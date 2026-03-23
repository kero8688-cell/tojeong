"""
토정비결 괘 계산 엔진

상괘(1-8): (세수 + 음력 생월) % 8  — 0이면 8
중괘(1-6): 음력 생월 % 6           — 0이면 6
하괘(1-3): 음력 생일 % 3           — 0이면 3

144가지 조합 = 8 × 6 × 3
"""
from .lunar import solar_to_lunar, get_korean_age


SANG_GWE_NAMES = {
    1: "건(乾)", 2: "태(兌)", 3: "리(離)", 4: "진(震)",
    5: "손(巽)", 6: "감(坎)", 7: "간(艮)", 8: "곤(坤)",
}

JUNG_GWE_NAMES = {
    1: "일(一)", 2: "이(二)", 3: "삼(三)",
    4: "사(四)", 5: "오(五)", 6: "육(六)",
}

HA_GWE_NAMES = {
    1: "초(初)", 2: "중(中)", 3: "말(末)",
}


def calculate_gwe(
    birth_solar_year: int,
    birth_solar_month: int,
    birth_solar_day: int,
    target_year: int,
) -> dict:
    """
    양력 생년월일과 운세 대상 연도를 받아 괘를 계산합니다.

    Returns:
        {
            "sang": int,   # 상괘 (1-8)
            "jung": int,   # 중괘 (1-6)
            "ha":   int,   # 하괘 (1-3)
            "key":  str,   # ex) "3-2-1"
            "lunar": dict, # 음력 생년월일
            "age":  int,   # 세수
            "sang_name": str,
            "jung_name": str,
            "ha_name":   str,
        }
    """
    lunar = solar_to_lunar(birth_solar_year, birth_solar_month, birth_solar_day)
    age = get_korean_age(lunar["year"], target_year)

    sang = (age + lunar["month"]) % 8
    if sang == 0:
        sang = 8

    jung = lunar["month"] % 6
    if jung == 0:
        jung = 6

    ha = lunar["day"] % 3
    if ha == 0:
        ha = 3

    return {
        "sang": sang,
        "jung": jung,
        "ha": ha,
        "key": f"{sang}-{jung}-{ha}",
        "lunar": lunar,
        "age": age,
        "sang_name": SANG_GWE_NAMES[sang],
        "jung_name": JUNG_GWE_NAMES[jung],
        "ha_name": HA_GWE_NAMES[ha],
    }
