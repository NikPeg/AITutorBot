import openai

from data.config import API_TOKEN

# Установите ваш API ключ
#
question = """На вход алгоритма подаётся натуральное число N. Алгоритм строит по нему новое число R следующим образом.
1.Строится двоичная запись числа N.
2.К этой записи дописываются справа ещё два разряда по следующему правилу:
а)складываются все цифры двоичной записи числа N, и остаток от деления суммы на 2 дописывается в конец числа (справа). Например, запись 11100 преобразуется в запись 111001;
б над этой записью производятся те же действий — справа дописывается остаток от деления суммы её цифр на 2.
Полученная таким образом запись (в ней на два разряда больше, чем в записи исходного числа N) является двоичной записью искомого числа R. Укажите минимальное число R, которое превышает число 97 и может являться результатом работы данного алгоритма. В ответе это число запишите в десятичной системе счисления.
"""
answer = """Поставить N к R"""

aa = """Алексей составляет таблицу кодовых слов для передачи сообщений, каждому сообщению соответствует своё кодовое слово. В качестве кодовых слов Алексей использует 5-буквенные слова, в которых есть только буквы A, B, C, X, причём буква X может появиться только на последнем месте или не появиться вовсе. Сколько различных кодовых слов может использовать Алексей?"""


def gpt_answer(question):
    client = openai.Client(api_key=API_TOKEN)
    prompt = f"Ответь на {question}"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model="gpt-3.5-turbo",
    )
    print(chat_completion)
    return chat_completion.choices[0].message.content


def evaluate_answer(title, numb, answer):
    print("a")
    file_ = open(f"./{title}/Задание{numb}.txt", "rb")
    contents = file_.read()
    client = openai.Client(api_key=API_TOKEN)
    prompt = f"Оцени решение на задание({contents}) и само решение:{answer} Напиши ошибки решения и как правильно нужно было решить:"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content


def main():
    import asyncio


if __name__ == "__main__":
    evaluate_answer(1, 1)
