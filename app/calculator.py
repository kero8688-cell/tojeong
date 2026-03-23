"""
토정비결 괘 계산 엔진

상괘(1-8): (세수 + 음력 생월) % 8  — 0이면 8
중괘(1-6): 음력 생월 % 6           — 0이면 6
하괘(1-3): (음력 생일 + 시주) % 3  — 0이면 3  (시주 미입력 시 0)

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

# 12지 시(時) — 2시간 단위
SI_NAMES = {
    0: "자시(子時) 23:00~01:00",
    1: "축시(丑時) 01:00~03:00",
    2: "인시(寅時) 03:00~05:00",
    3: "묘시(卯時) 05:00~07:00",
    4: "진시(辰時) 07:00~09:00",
    5: "사시(巳時) 09:00~11:00",
    6: "오시(午時) 11:00~13:00",
    7: "미시(未時) 13:00~15:00",
    8: "신시(申時) 15:00~17:00",
    9: "유시(酉時) 17:00~19:00",
    10: "술시(戌時) 19:00~21:00",
    11: "해시(亥時) 21:00~23:00",
}


def hour_to_si(hour: int) -> int:
    """시각(0~23) → 12지 시 인덱스(0~11)"""
    if hour == 0 or hour == 23:
        return 0  # 자시
    return (hour + 1) // 2


def calculate_gwe(
    birth_solar_year: int,
    birth_solar_month: int,
    birth_solar_day: int,
    target_year: int,
    birth_hour: int = -1,   # -1: 모름, 0~23: 출생 시각
    birth_minute: int = 0,  # 0 또는 30
) -> dict:
    """
    양력 생년월일(+출생 시각)과 운세 대상 연도를 받아 괘를 계산합니다.

    birth_hour == -1 이면 시각 미입력으로 처리 (시주 보정 없음).
    """
    lunar = solar_to_lunar(birth_solar_year, birth_solar_month, birth_solar_day)
    age = get_korean_age(lunar["year"], target_year)

    sang = (age + lunar["month"]) % 8
    if sang == 0:
        sang = 8

    jung = lunar["month"] % 6
    if jung == 0:
        jung = 6

    # 시주 보정: 출생 시각이 있으면 12지 시 인덱스를 하괘에 반영
    si_index = -1
    si_name = "모름"
    if birth_hour >= 0:
        si_index = hour_to_si(birth_hour)
        si_name = SI_NAMES[si_index]
        ha = (lunar["day"] + si_index) % 3
    else:
        ha = lunar["day"] % 3
    if ha == 0:
        ha = 3

    # 출생 시각 표시 문자열
    if birth_hour >= 0:
        birth_time_str = f"{birth_hour:02d}:{birth_minute:02d}"
    else:
        birth_time_str = "모름"

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
        "si_index": si_index,
        "si_name": si_name,
        "birth_time_str": birth_time_str,
    }
