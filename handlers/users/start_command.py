import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import get_files_count, ref_info, ref_title, teach_ref, teachers_id
from database.user_db import (
    add_new_user,
    add_new_work,
    check_name_in_file,
    get_all_students,
    get_all_taken_user_info,
    get_student_name,
    get_user_info,
    get_user_ref, check_user,
)
from keyboards.user_keyboards import *
from loader import bot, dp, proxy
from states.User import User_
from utils.mess import *


@dp.callback_query_handler(text="return")
async def return_call_handler(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.message.chat.id, return_text, reply_markup=user_markup())


@dp.message_handler(commands=["start"], state="*")
async def start_command_handler(message: types.Message, state: FSMContext):
    if str(message.text[7:]):
        async with state.proxy() as data:
            data["ref"] = message.text[7:]
        ref_ = ref_title[message.text[7:]]
        start_mes = start_mess(ref_)
        await bot.send_message(message.chat.id, f"{start_mes}")
        await User_.name.set()
    else:
        ref_ = get_user_ref(message.chat.id)
        text = ref_text(ref_)
        await bot.send_message(message.chat.id, text, reply_markup=user_markup())


@dp.message_handler(state=User_.name)
async def user_name_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ref = data["ref"]
    check_ = check_name_in_file(message.text.lower())
    if check_ == False:
        await bot.send_message(message.chat.id, error_mess)
        await User_.name.set()
    else:
        add_new_user(message.chat.id, message.text, ref)
        await state.finish()
        text = ref_text(ref)
        await bot.send_message(message.chat.id, text, reply_markup=user_markup())


@dp.callback_query_handler(text="userworks")
async def userworks_handler(call: types.CallbackQuery):
    ref = get_user_ref(call.message.chat.id)
    files_count = get_files_count(ref)
    for numb in range(1, files_count):
        await bot.send_message(call.message.chat.id, work_count(numb), reply_markup=user_t_markup(numb))
    await bot.send_message(call.message.chat.id, send_mess)


@dp.callback_query_handler(text_startswith="send_")
async def ref_info_call(call: types.CallbackQuery, state: FSMContext):
    numb = call.data[5:]
    async with state.proxy() as data:
        data["numb"] = numb
    await bot.send_message(call.message.chat.id, send_r)
    await User_.task.set()


@dp.callback_query_handler(text_startswith="ask_")
async def answer_call_handler(call: types.CallbackQuery):
    await call.answer()
    numb = call.data[4:]
    await bot.send_message(call.message.chat.id, question_mess(numb), reply_markup=user_return_markup())
    await User_.question.set()


@dp.message_handler(state=User_.question)
async def answer_on_question(message: types.Message, state: FSMContext):
    from gpt_func import gpt_answer

    await state.finish()
    answer = gpt_answer(message.text)
    await bot.send_message(message.chat.id, answer, reply_markup=user_return_markup())


evaluates_ = {}


@dp.message_handler(state=User_.task)
async def usertask_handler(message: types.Message, state: FSMContext):
    global evaluates_
    async with state.proxy() as data:
        numb = data["numb"]
    await state.finish()
    from gpt_func import evaluate_answer

    ref = get_user_ref(message.chat.id)
    teacher_id = teach_ref[ref]
    title = ref_title[ref]
    user_name = get_student_name(message.chat.id)
    mess = await bot.send_message(teacher_id, teach_recive(user_name, numb, message.text))
    add_new_work(message.chat.id, mess.message_id, numb)
    # info = evaluate_answer(title, numb, message.text)
    thread = proxy.create_thread()
    proxy.add_message(thread, message.text)
    info = await proxy.get_answer(thread)
    evaluates_[teacher_id] = info
    await bot.send_message(teacher_id, ii_check)
    await bot.send_message(teacher_id, f"{info}", reply_markup=t_check_markup(message.chat.id, numb))
    await bot.send_message(message.chat.id, check_t)


@dp.callback_query_handler(text_startswith="allow_", state="*")
async def allow_send_call_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    global evaluates_
    user_info = call.data.split("_")
    await bot.send_message(
        user_info[1], student_recive(user_info[2], evaluates_[call.message.chat.id]), reply_markup=user_return_markup()
    )
    await state.finish()
    await bot.send_message(call.message.chat.id, send_student)


@dp.callback_query_handler(text_startswith="no_", state="*")
async def no_call_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user_info = call.data.split("_")
    async with state.proxy() as data:
        data["user_id"] = user_info[1]
        data["numb"] = user_info[2]
    await bot.send_message(call.message.chat.id, write_answer)
    await User_.teacher.set()


@dp.message_handler(state=User_.teacher)
async def user_teacher_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data["user_id"]
        numb = data["numb"]
    await state.finish()
    await bot.send_message(user_id, student_recive(numb, message.text), reply_markup=user_return_markup())
    await bot.send_message(message.chat.id, send_student)
    # add_new_work(user_id,f"")


@dp.message_handler(commands=["teach"], chat_id=teachers_id)
async def teach_command_handler(message: types.Message):
    await bot.send_message(message.chat.id, start_teach_mess, reply_markup=t_menu())


@dp.callback_query_handler(text="all")
async def all_students_handler(call: types.CallbackQuery):
    await call.message.edit_text(text=all_students_)
    ref_ = ref_info[call.message.chat.id]
    all_students = get_all_students(ref_)
    for student in all_students:
        text_ = f"{student[0]}\n" f"✅Запустил бота\n\n"
        await bot.send_message(call.message.chat.id, text_, reply_markup=user_info(student[1]))
        await asyncio.sleep(0.1)


@dp.callback_query_handler(text_startswith="info_")
async def ref_info_call(call: types.CallbackQuery):
    user_id = call.data[5:]
    await call.message.delete()
    student_name = get_student_name(user_id)
    user_info_ = get_user_info(user_id)
    if user_info_ == False:
        await bot.send_message(call.message.chat.id, no_send_(student_name))
    else:
        await bot.send_message(call.message.chat.id, taken_list(student_name))
        for info in user_info_:
            await bot.send_message(call.message.chat.id, f"{student_name}", reply_to_message_id=info[0])
            # await bot.send_message(call.message.chat.id, f"{info[0]}")


@dp.callback_query_handler(text_startswith="take_")
async def all_take_students(call: types.CallbackQuery):
    numb = call.data[5:]
    info = ref_info[call.message.chat.id]
    all_info = get_all_taken_user_info(info, numb)
    if all_info == False:
        await call.answer(none_taken)
    for info in all_info:
        await call.answer()
        await bot.send_message(call.message.chat.id, f"{info[0]}", reply_to_message_id=info[1])
        await asyncio.sleep(0.1)


@dp.callback_query_handler(text="works")
async def all_works_handler(call: types.CallbackQuery):
    await call.answer()
    ref = ref_info[call.message.chat.id]
    files_count = get_files_count(ref)
    for numb in range(1, files_count):
        await bot.send_message(call.message.chat.id, work_count(numb), reply_markup=take_markup(numb))


@dp.callback_query_handler(text="link")
async def link_call(call: types.CallbackQuery):
    await call.answer()
    ref_ = ref_info[call.message.chat.id]
    await bot.send_message(call.message.chat.id, reflink(ref_))
