import asyncio
import aiohttp


async def get_color_name_async(hex_color):

    url = f"https://www.thecolorapi.com/id?hex={hex_color}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            color_name = data.get("name", {}).get("value")
            return color_name


async def main():
    hex_color = "FFFFF9"  # Пример HEX-значения цвета
    color_name = await get_color_name_async(hex_color)
    print(f"The color name for {hex_color} is: {color_name}")


asyncio.run(main())
