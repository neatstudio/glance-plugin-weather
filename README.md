# glance-plugin-weather

Current weather from [Open-Meteo](https://open-meteo.com/) (no API key) for
the [glance](https://github.com/neatstudio/glance) hub.

Install: paste `github:neatstudio/glance-plugin-weather@v1.0.0` into the
hub's 插件 page, or pick `weather` from the index.

Entity `weather.now`: `temp` (°C), `text` (晴 / 多云 / 雨 …), `code`
(WMO weather code), `line` (`上海 21C 晴`). Settings: latitude, longitude,
city label, refresh interval. Permission: `network`.
