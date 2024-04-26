from aiogram import Router, types


def reverse_words(message):
    words = message.split()
    reversed_words = words[::-1]
    reversed_message = ' '.join(reversed_words)
    return reversed_message


echo_router = Router()


@echo_router.message()
async def echo(message: types.Message):
    reversed_message = reverse_words(message.text)
    await message.answer(reversed_message)