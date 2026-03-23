"""
양력 → 음력 변환 모듈
korean-lunar-calendar 라이브러리 사용
"""
from korean_lunar_calendar import KoreanLunarCalendar


def solar_to_lunar(year: int, month: int, day: int) -> dict:
    """
    양력 날짜를 음력으로 변환
    Returns: {"year": int, "month": int, "day": int, "is_leap": bool}
    """
    cal = KoreanLunarCalendar()
    cal.setSolarDate(year, month, day)
    return {
        "year": cal.lunarYear,
        "month": cal.lunarMonth,
        "day": cal.lunarDay,
        "is_leap": cal.isIntercalation,
    }


def get_korean_age(birth_year: int, target_year: int) -> int:
    """한국식 나이(세수) 계산"""
    return target_year - birth_year + 1
