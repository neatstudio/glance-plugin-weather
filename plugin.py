"""Weather source: Open-Meteo current conditions → entity `weather.now`.

Reference plugin for 02-plugin-package.md. Everything it needs comes
through `ctx`; it reads no environment variables and no files.
"""

from __future__ import annotations

from glance.plugin import SourcePlugin

URL = "https://api.open-meteo.com/v1/forecast"
LABELS = (
    ({0}, "晴"),
    ({1, 2, 3}, "多云"),
    ({45, 48}, "雾"),
    ({51, 53, 55, 61, 63, 65, 80, 81, 82}, "雨"),
    ({71, 73, 75, 85, 86}, "雪"),
    ({95, 96, 99}, "雷"),
)


def label(code: int | None) -> str:
    for codes, text in LABELS:
        if code in codes:
            return text
    return ""


class Weather(SourcePlugin):
    async def start(self) -> None:
        self.ctx.every(int(self.ctx.settings["refresh_min"]) * 60, self.refresh)

    async def refresh(self) -> None:
        settings = self.ctx.settings
        response = await self.ctx.http.get(
            URL,
            params={
                "latitude": settings["latitude"],
                "longitude": settings["longitude"],
                "current": "temperature_2m,weather_code",
                "timezone": "auto",
            },
            timeout=8.0,
        )
        response.raise_for_status()
        current = response.json().get("current") or {}
        temp = current.get("temperature_2m")
        code = current.get("weather_code")
        text = label(code)
        line = f"{settings['city']} {temp:.0f}C {text}" if temp is not None else f"{settings['city']} {text}"
        self.ctx.entities.publish("now", {"temp": temp, "text": text, "code": code, "line": line})


def create(ctx) -> Weather:
    return Weather(ctx)
