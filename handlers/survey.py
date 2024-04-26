from aiogram import Router, F, types
from config import database
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


survey_router = Router()


class BookSurvey(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    salary_or_grade = State()


@survey_router.message(Command("stop"))
@survey_router.message(F.text.lower() == "стоп")
async def stop(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Спасибо за прохождение опроса!")


@survey_router.message(Command('review'))
async def start_review(message: types.Message, state: FSMContext):
    await state.set_state(BookSurvey.name)
    await message.answer('Как вас зовут?')


@survey_router.message(BookSurvey.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookSurvey.age)
    await message.answer(f"Сколько вам лет, {message.text}?")


@survey_router.message(BookSurvey.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Пожалуйста, введите число")
        return
    await state.update_data(age=int(age))
    await state.set_state(BookSurvey.occupation)
    await message.answer("Укажите занятие?")


@survey_router.message(BookSurvey.occupation)
async def process_occupation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    age = data.get('age')
    await state.update_data(occupation=message.text)
    await state.set_state(BookSurvey.salary_or_grade)
    if int(age) < 15:
        await message.answer("Какая у вас оценка в школе?")
    else:
        await message.answer("Какая у вас заработная плата?")


@survey_router.message(BookSurvey.salary_or_grade)
async def process_sog(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print("-", data)
    await database.execute(
        "INSERT INTO survey (name, age, occupation, salary_or_grade) VALUES (?, ?, ?, ?)", 
        (data["name"], data["age"], data["occupation"], data["salary_or_grade"])
    )
    await message.answer("Спасибо за пройденный опрос!")
    await state.clear()