import asyncio
from collections import namedtuple

import httpx


class WeatherFetcher:
    def __init__(self, queue: asyncio.Queue) -> None:
        self.queue = queue

    async def gather_data(self) -> None:
        while True:
            try:
                weather_data = await self._make_api_call()
            except httpx.HTTPError:
                continue
            parsed_data = await self._parse_data(weather_data)
            await self.queue.put(parsed_data)
            await asyncio.sleep(10)

    @staticmethod
    async def _make_api_call() -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.open-meteo.com/v1/forecast?latitude=51.10&longitude=17.03&hourly=temperature_2m,rain"
            )
        response.raise_for_status()
        return response.json()

    @staticmethod
    async def _parse_data(weather_data: dict) -> map:
        weather = namedtuple('Weather', ['time', 'temp', 'rain'])
        hourly_weather = weather_data.get('hourly', dict())
        return map(
            lambda time, temp, rain: weather(time, temp, rain),
            hourly_weather.get('time', []),
            hourly_weather.get('temperature_2m', []),
            hourly_weather.get('rain', [])
        )
