from aiogram.types import ParseMode

from .formatting import markdown_to_html, escape_symbols, escape_markdown_symbols

from data.config import ADMIN_ID

MAX_MESSAGE_LENGTH = 4096 - 10
SPECIAL_SYMBOLS = ["*", "_", "~"]


async def send_big_message(bot, user_id, text, reply_markup=None):
    if not text:
        return
    symbols_stack = []
    code_mode = False
    big_code_mode = False
    text = escape_markdown_symbols(text)
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        text_part = ""
        j = 0
        if big_code_mode:
            text_part += "```"
            j += 3
        elif code_mode:
            text_part += "`"
            j += 1
        else:
            for symbol in symbols_stack:
                text_part += symbol
        text_part += text[i:i + MAX_MESSAGE_LENGTH]
        while j < len(text_part):
            if j + 3 <= len(text_part) and text_part[j:j + 3] == "```":
                big_code_mode = not big_code_mode
                j += 3
                continue
            if text_part[j] == "`":
                code_mode = not code_mode
                j += 1
                continue
            if not code_mode and j + 2 <= len(text_part) and text_part[j:j + 2] == "__":
                if symbols_stack and symbols_stack[-1] == "__":
                    symbols_stack.pop()
                else:
                    symbols_stack.append("__")
                j += 2
                continue
            if not code_mode and not big_code_mode and text_part[j] in SPECIAL_SYMBOLS:
                if symbols_stack and symbols_stack[-1] == text_part[j]:
                    symbols_stack.pop()
                else:
                    symbols_stack.append(text_part[j])
            j += 1
        if big_code_mode:
            text_part += "```"
        elif code_mode:
            text_part += "`"
        else:
            for symbol in symbols_stack[::-1]:
                text_part += symbol
        try:
            await bot.send_message(user_id, text_part, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=reply_markup)
            continue
        except Exception as e:
            await bot.send_message(ADMIN_ID, e)
            print(e)
        for parse_mode in [ParseMode.MARKDOWN, ParseMode.HTML]:
            try:
                await bot.send_message(user_id, text_part, parse_mode=parse_mode, reply_markup=reply_markup)
                break
            except Exception as e:
                await bot.send_message(ADMIN_ID, e)
                print(e)
        else:
            try:
                await bot.send_message(user_id, markdown_to_html(text_part), parse_mode=ParseMode.HTML, reply_markup=reply_markup)
                continue
            except Exception as e:
                await bot.send_message(ADMIN_ID, e)
                print(e)
            try:
                await bot.send_message(user_id, escape_symbols(text_part), reply_markup=reply_markup)
                continue
            except Exception as e:
                await bot.send_message(ADMIN_ID, e)
                print(e)
