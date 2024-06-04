import time

import openai
from openai import AsyncOpenAI
from openai.types.beta.assistant_create_params import ToolResources, ToolResourcesFileSearch, \
    ToolResourcesFileSearchVectorStore

import prompts

try:
    from data.config import ASSISTANT_ID
except ImportError:
    ASSISTANT_ID = None
except AttributeError:
    ASSISTANT_ID = None

try:
    from data.config import FILE_ID
except ImportError:
    FILE_ID = None
except AttributeError:
    FILE_ID = None


class GPTProxy:
    def __init__(self, token, model="gpt-4o", bot=None):
        self.client = openai.OpenAI(api_key=token)
        self.model = model
        if not FILE_ID:
            file_id = self.upload_file("info/only_task1.docx")
        else:
            file_id = FILE_ID
        if not ASSISTANT_ID:
            self.assistant_id = self.create_assistant("ai tutor", prompts.TUTOR, [file_id])
        else:
            self.assistant_id = ASSISTANT_ID
        self.bot = bot
        self.aclient = AsyncOpenAI(api_key=token)

    def upload_file(self, path, purpose="assistants"):
        result = self.client.files.create(
            file=open(path, "rb"),
            purpose=purpose,
        )
        print(result.id)
        return result.id

    def create_assistant(self, name, instructions, file_ids):
        assistant = self.client.beta.assistants.create(
            model=self.model,
            name=name,
            tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
            instructions=instructions,
            tool_resources=ToolResources(file_search=ToolResourcesFileSearch(vector_stores=[
                ToolResourcesFileSearchVectorStore(file_ids=file_ids)])),
        )
        print("assistant_id:", assistant.id)
        return assistant.id

    async def add_message(self, thread_id, user_question=" ", photo_paths=None, file_paths=None):
        photo_paths = [] if not photo_paths else photo_paths
        file_paths = [] if not file_paths else file_paths
        await self.aclient.beta.threads.messages.create(
            thread_id=thread_id,
            content=[
                        {
                            "text": user_question,
                            "type": "text",
                        },
                    ] + [
                        {
                            "type": "image_file",
                            "image_file": {
                                "file_id": self.upload_file(path, "vision"),
                                "detail": "low",
                            }
                        } for path in photo_paths
                    ] or " ",
            role="user",
            attachments=[{"file_id": self.upload_file(path), "tools": [{"type": "file_search"}]} for path in file_paths],
        )

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
