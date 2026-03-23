import json
import os
from datetime import date

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.calculator import calculate_gwe

BASE_DIR = os.path.dirname(__file__)

# 운세 DB 로드
with open(os.path.join(BASE_DIR, "app", "data", "fortunes.json"), encoding="utf-8") as f:
    FORTUNES: dict = json.load(f)

app = FastAPI(title="토정비결")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "current_year": date.today().year,
    })


@app.post("/result", response_class=HTMLResponse)
async def result(
    request: Request,
    birth_year:   int  = Form(...),
    birth_month:  int  = Form(...),
    birth_day:    int  = Form(...),
    target_year:  int  = Form(...),
    gender:       str  = Form("남"),
    name:         str  = Form(""),
    birth_time:   str  = Form("-1"),   # "-1": 모름, "HH:MM" 형식
):
    # 출생 시각 파싱
    birth_hour, birth_minute = -1, 0
    if birth_time and birth_time != "-1":
        try:
            h, m = birth_time.split(":")
            birth_hour, birth_minute = int(h), int(m)
        except ValueError:
            pass

    try:
        gwe = calculate_gwe(birth_year, birth_month, birth_day, target_year,
                            birth_hour, birth_minute)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"날짜 변환 오류: {e}")

    fortune = FORTUNES.get(gwe["key"])
    if not fortune:
        raise HTTPException(status_code=404, detail="해당 괘를 찾을 수 없습니다.")

    # 등급별 색상
    grade_color = {
        "대길(大吉)": "#c0392b",
        "길(吉)":     "#e67e22",
        "중길(中吉)": "#27ae60",
        "평(平)":     "#2980b9",
        "중흉(中凶)": "#8e44ad",
        "흉(凶)":     "#555",
        "대흉(大凶)": "#2c3e50",
    }.get(fortune["grade"], "#2c3e50")

    return templates.TemplateResponse("result.html", {
        "request":     request,
        "name":        name or "귀하",
        "gender":      gender,
        "birth":       f"{birth_year}년 {birth_month}월 {birth_day}일 (양력)",
        "birth_time":  gwe["birth_time_str"],
        "target_year": target_year,
        "gwe":         gwe,
        "fortune":     fortune,
        "grade_color": grade_color,
    })
