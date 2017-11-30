import os

import aiohttp
from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)
TELEGRAM_KEY = os.environ.get('TELEGRAM_KEY')
ANSWERS = [
    'Человечек не захочет, кабанчик не вскочит',
    'Стоит обкашлять с братанами',
    'Лучше съездий на шашлындосы в центре',
    'Обязательно провентелируй',
    'Ставлю на контроль',
    'Все чин чинарем',
    'Цифры наберуться',
    'Добро',
    'Тема мутная',
    'Чет не фунциклирует',
    'Всё в ажуре',
    'Вопросик на тормозах',
    'Да, но с тебя поляна',
    'Тоси боси',
]


async def send_tg_message(chat_id, message):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'https://api.telegram.org/bot{TELEGRAM_KEY}/sendMessage/',
            json={"chat_id": chat_id, "text": message}
        ) as resp:
            return await resp.json()


@app.route('/', methods=['POST'])
async def get_msg(request):
    data = request.json
    message = data['message']
    chat_id = message['chat']['id']
    message_txt = message['text']

    index = sum([ord(c) for c in message_txt]) % len(ANSWERS)
    answer = ANSWERS[index]

    await send_tg_message(chat_id, answer)

    return json({})
