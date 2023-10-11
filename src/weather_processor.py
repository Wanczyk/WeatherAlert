import asyncio


class WeatherProcessor:
    def __init__(self, queue: asyncio.Queue, temp_threshold: float, rain_threshold: float) -> None:
        self.queue = queue
        self.temp_threshold = temp_threshold
        self.rain_threshold = rain_threshold

    async def process_data(self) -> None:
        while True:
            item = await self.queue.get()
            await self._alert(item)

    async def _alert(self, weather_data) -> None:
        for data in weather_data:
            messages = []
            if data.temp <= self.temp_threshold:
                messages.append(f"low temperature {data.temp} of C")
            if data.rain >= self.rain_threshold:
                messages.append(f"rain {data.rain} mm")
            if messages:
                message = " and ".join(messages)
                print(f"Warning Wroclaw, {message} expected on {data.time}")

