import asyncio
from unittest import mock

import pytest
from httpx import Response, Request

from src.weather_fetcher import WeatherFetcher


class TestWeatherFetcher:
    @pytest.mark.asyncio
    @mock.patch('src.weather_fetcher.httpx.AsyncClient.get')
    async def test_gather_data(self, async_client_patch):
        async_client_patch.side_effect = [
            Response(200, request=Request("POST", "test"), json={
                "latitude": 51.1,
                "longitude": 17.039999,
                "generationtime_ms": 0.21708011627197266,
                "utc_offset_seconds": 0,
                "timezone": "GMT",
                "timezone_abbreviation": "GMT",
                "elevation": 118.0,
                "hourly_units": {
                    "time": "iso8601",
                    "temperature_2m": "°C",
                    "rain": "mm"
                },
                "hourly": {
                    "time": [
                        "2023-10-11T00:00",
                        "2023-10-11T01:00",
                        "2023-10-11T02:00"
                    ],
                    "temperature_2m": [
                        12.3,
                        12.5,
                        12.8
                    ],
                    "rain": [
                        0.00,
                        0.00,
                        0.00
                    ]
                }
            }),
            Response(200, request=Request("POST", "test"), json={
                "latitude": 51.1,
                "longitude": 17.039999,
                "generationtime_ms": 0.21708011627197266,
                "utc_offset_seconds": 0,
                "timezone": "GMT",
                "timezone_abbreviation": "GMT",
                "elevation": 118.0,
                "hourly_units": {
                    "time": "iso8601",
                    "temperature_2m": "°C",
                    "rain": "mm"
                },
                "hourly": {
                    "time": [
                        "2023-10-11T00:00",
                        "2023-10-11T01:00",
                        "2023-10-11T02:00"
                    ],
                    "temperature_2m": [
                        13.3,
                        13.5,
                        13.8
                    ],
                    "rain": [
                        1.00,
                        2.00,
                        3.00
                    ]
                }
            })
        ]
        queue = asyncio.Queue()
        weather_fetcher = WeatherFetcher(queue)
        producer_task = asyncio.create_task(weather_fetcher.gather_data())
        await asyncio.sleep(15)
        producer_task.cancel()

        assert queue.qsize() == 2
