import openai
import prompts
from data.config import ADMIN
from openai import OpenAI, AsyncOpenAI
import time


class GPTProxy:
    def __init__(self, token, model="gpt-4-0125-preview", bot=None):
        self.client = openai.OpenAI(api_key=token)
        self.model = model
        file_id = self.upload_file("info/task1.docx")
        self.assistant_id = self.create_assistant("ai tutor", prompts.TUTOR, [file_id])
        # self.assistant_id = "asst_VU7qla6AwkAIk7W3vwqLZn8s"
        self.bot = bot
        self.aclient = AsyncOpenAI(api_key=token)

    def upload_file(self, path, purpose="assistants"):
        # result = self.client.files.create(
        #     file=open(path, "rb"),
        #     purpose=purpose,
        # )
        # print(result.id)
        return "file-cHcCruOy41OWwCEEqCjvWm3G"
        # return result.id

    def create_assistant(self, name, instructions, file_ids):
        assistant = self.client.beta.assistants.create(
            model=self.model,
            name=name,
            tools=[{"type": "retrieval"}],
            instructions=instructions,
            file_ids=file_ids,
        )
        print("assistant_id:", assistant.id)
        # assistant_id = "asst_rlBcham3icvPpcgnEWmqJf86"
        return assistant.id

    async def add_message(self, thread_id, user_question):
        message = await self.aclient.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content= user_question
        )
        return message

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread.id

    async def get_answer(self, thread_id, func=None):
        run = await self.aclient.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
        )
        while True:
            if func:
                await func()
            run_info = await self.aclient.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_info.completed_at:
                break
            time.sleep(1)
        messages = await self.aclient.beta.threads.messages.list(thread_id)
        assistant_messages = []
        for message_data in messages.data:
            if message_data.role == "assistant":
                assistant_messages.append(message_data.content[0].text.value)
            else:
                break
        return "".join(assistant_messages[::-1])
