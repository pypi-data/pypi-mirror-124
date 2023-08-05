import aiohttp
from PIL import Image, ImageDraw, ImageFont
import urllib.request, textwrap, asyncio, json

async def get_image(*, font_name, font_size=100, image_api_url='https://picsum.photos/1600/900', margin=35, fill_color='#ffffff', format="q - a", file_format="png"):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://zenquotes.io/api/random') as response:
            response = json.loads(await response.text())
            options = {
            "q - a" : (f"{response[0]['q']} - {response[0]['a']}"),
            "q \n a": (f"{response[0]['q']}\n{response[0]['a']}"),
            "q": (f"{response[0]['q']}"),
            }

            text = options[format]


    urllib.request.urlretrieve(image_api_url, f'image.{file_format}')

    img = Image.open(f'image.{file_format}')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_name, font_size)
    margin = offset = margin
    for line in textwrap.wrap(text, width=margin):
        draw.text((margin, offset), line, font=font, fill=fill_color)
        offset += font.getsize(line)[1]

    img.save(f'image.{file_format}')