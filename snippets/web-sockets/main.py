"""Dunder Mifflin PA System: two WebSocket channels and one page.

Run: uv run uvicorn main:app --reload
"""

import asyncio
from datetime import datetime, timezone
from itertools import count
from pathlib import Path
from random import choice, randint
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="Dunder Mifflin PA System")

PAGE = Path(__file__).parent / "static" / "index.html"
CHECKIN_POINTS = 5
EMPLOYEES = {
    "Michael": "That's what she said!",
    "Dwight": "FALSE.",
    "Stanley": "Did I stutter?",
    "Kevin": "Why waste time say lot word?",
    "Oscar": "Actually...",
    "Angela": "My cats would disagree.",
}
MOODS = {"happy": "😁", "angry": "😡", "insightful": "🤔"}
ITEMS = [
    ("🏆", "Dundie Award", 50),
    ("☕", "World's Best Boss Mug", 25),
    ("🐻", "Recyclops Costume Piece", 30),
    ("📎", "Stapler in Jello", 15),
    ("🧀", "Party Planning Committee Cheese", 5),
    ("🥨", "Pretzel Day Pretzel", 8),
    ("🥧", "Schrute Farms Beet", 10),
    ("📠", "Fax From Future Dwight", 20),
]


def now() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def reply(text: str) -> str:
    employee, catchphrase = choice(list(EMPLOYEES.items()))
    return f'{employee}: "{catchphrase}" (heard "{text}" at {now()} UTC)'


def make_event(socket_id: str, number: int) -> dict:
    employee = choice(list(EMPLOYEES))
    if randint(0, 1):
        mood, emoji = choice(list(MOODS.items()))
        kind, detail, bucks = "check-in", f"{emoji} {mood}", CHECKIN_POINTS
    else:
        emoji, name, cost = choice(ITEMS)
        kind, detail, bucks = "redeem", f"{emoji} {name}", -cost
    return {
        "socket_id": socket_id,
        "count": number,
        "type": kind,
        "employee": employee,
        "detail": detail,
        "schrute_bucks": bucks,
        "at": now(),
    }


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    return HTMLResponse(PAGE.read_text(encoding="utf8"))


@app.websocket("/ws/intercom")
async def intercom(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            text = await websocket.receive_text()
            if text.strip() == "close":
                await websocket.close()
                return
            await websocket.send_text(reply(text))
    except WebSocketDisconnect:
        return


@app.websocket("/ws/ticker")
async def ticker(websocket: WebSocket) -> None:
    await websocket.accept()
    socket_id = str(uuid4())
    try:
        for number in count(1):
            await asyncio.sleep(choice([1, 3, 5]))
            await websocket.send_json(make_event(socket_id, number))
    except WebSocketDisconnect:
        return
