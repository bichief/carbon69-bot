from aiogram import types

from loader import dp


@dp.inline_handler(text='')
async def empty_query(query: types.InlineQuery):
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id='unknown',
                title='Тут ничего нет',
                input_message_content=types.InputTextMessageContent(
                    message_text='Я зачем-то нажал на эту кнопку :('
                ),
                description='тут тоже пусто',

            )
        ],
        cache_time=5
    )

@dp.inline_handler(text='new_administrator')
async def new_admin(query: types.InlineQuery):
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id='1',
                title='Поделиться ссылкой',
                description='Поделившись, он станет админом в Боте',
                input_message_content=types.InputTextMessageContent(
                    message_text='t.me/Carbon69Bot?start=20344839jfksWRIWOR'
                )
            )
        ]
    )