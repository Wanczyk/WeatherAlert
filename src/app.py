import asyncio

from src.weather_fetcher import WeatherFetcher
from src.weather_processor import WeatherProcessor


async def app(temp_threshold, rain_threshold):
    queue = asyncio.Queue()

    weather_processor = WeatherProcessor(queue, temp_threshold, rain_threshold)
    weather_fetcher = WeatherFetcher(queue)

    producer_task = asyncio.create_task(weather_fetcher.gather_data())
    consumer_task = asyncio.create_task(weather_processor.process_data())

    await asyncio.gather(producer_task, consumer_task)
