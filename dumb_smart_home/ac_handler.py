import os
from typing import Optional

import requests
from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/handle_ac")
def handle_ac(
    power: str,
    mode: Optional[str],
    temp: Optional[int],
    fan_mode: Optional[str],
    timer_on: Optional[int],
    timer_off: Optional[int],
    swing: Optional[bool] = False,
    comfort: Optional[bool] = False,
):
    payload = {
        "auth_key": os.getenv("AC_AUTH_KEY"),
        "power": power,
    }
    if power == "on":
        payload = payload | {
            "mode": mode,
            "fanMode": fan_mode,
            **({"temp": temp} if mode != "fan" else {}),
            **({"timerOn": timer_on} if timer_on else {}),
            **({"timerOff": timer_off} if timer_off else {}),
            **({"swing": swing} if swing else {}),
            **({"comfort": comfort} if comfort else {}),
        }
    response = requests.put(
        "http://" + os.getenv("AC_IP_ADDRESS"),
        json=payload,
    )
    return RedirectResponse("/")
