import asyncio
from collections import namedtuple

import pytest

from src.weather_processor import WeatherProcessor


class TestWeatherProcessor:
    @pytest.mark.asyncio
    async def test_process_data(self, capsys):
        weather = namedtuple('Weather', ['time', 'temp', 'rain'])
        queue = asyncio.Queue()
        weather_processor = WeatherProcessor(queue, temp_threshold=10.0, rain_threshold=5.0)

        weather_data = [
            weather("2023-10-11 12:00", 1.0, 0.0),
            weather("2023-10-11 15:00", 15.0, 1.0),
        ]
        await queue.put(weather_data)

        weather_data = [
            weather("2023-10-12 12:00", 1.0, 6.0),
            weather("2023-10-12 15:00", 15.0, 5.0),
        ]
        await queue.put(weather_data)

        consumer_task = asyncio.create_task(weather_processor.process_data())
        await asyncio.sleep(1)
        consumer_task.cancel()
        captured = capsys.readouterr()

        assert queue.qsize() == 0
        assert captured.out == (
            'Warning Wroclaw, low temperature 1.0 of C expected on 2023-10-11 12:00\n'
            'Warning Wroclaw, low temperature 1.0 of C and rain 6.0 mm expected on 2023-10-12 12:00\n'
            'Warning Wroclaw, rain 5.0 mm expected on 2023-10-12 15:00\n'
        )
