from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from generators.generators import generate

class Work(StatesGroup):
    process = State()

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message,  state: FSMContext):
    await message.answer('Велкомьте :)\nНапишите ваш запрос')
    await state.clear()

@router.message(Command(commands='help'))
async def cmd_help(message: Message):
    await message.answer('Это чат-бот с ИИ, просто напишите сообщение и вы получите на него ответ. Для использования даннного бота в России не нужен VPN и прочие средства обхода блокировок. Используется модель Mistral, которая по функционалу похожа на ChatGPT, она, конечно, не умеет пока что генерировать картинки, но зато разработчику этого бота не приходиться возиться с прокси и тратить деньги на токены (не в обиду чатуGPT) :)')

@router.message()
async def ai(message: Message, state: FSMContext):
    await state.set_state(Work.process)
    res = await generate(message.text)
    await message.answer(res.choices[0].message.content)
    await state.clear()

@router.message()
async def stop(message: Message):
    await message.answer('Подождите, прошлый ответ ещё генерируется...')