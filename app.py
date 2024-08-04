import chainlit as cl
import chainlit.data as cl_data
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.types import ThreadDict
import os
from minio import MinioStorageClient

cl_data._data_layer = SQLAlchemyDataLayer(conninfo=os.environ["PG_CONNECTION_STRING"],storage_provider=MinioStorageClient(bucket="chainlit",endpoint_url="http://localhost:9000",aws_access_key_id="minio",aws_secret_access_key="minio123",verify_ssl=False))

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    print(thread)
    await cl.Message(content=thread.name, author="user").send()

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None
    
@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="邯郸今日x新闻",
            message="请提供下今日邯郸新闻",
            icon="/public/logo_light.png",
            ),

        cl.Starter(
            label="今日大事记",
            message="请提供下今日大事记",
            icon="/public/logo_light.png",
            ),
        cl.Starter(
            label="今日总结报告",
            message="请提供下今日总结报告",
            icon="/public/logo_light.png",
            ),
        cl.Starter(
            label="任务配置",
            message="请提供下任务配置",
            icon="/public/logo_light.png",
            )
        ]

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="GPT-3.5",
            markdown_description="The underlying LLM model is **GPT-3.5**.",
            icon="/public/logo_light.png",
        ),
        cl.ChatProfile(
            name="GPT-4",
            markdown_description="The underlying LLM model is **GPT-4**.",
            icon="/public/logo_light.png",
        ),
    ]


@cl.step(name="x大事记",type="x消息工具")
async def tool():
    # Simulate a running task
    await cl.sleep(2)
    return "Response from the tool!"


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...

    # Send a response back to the user
    # await cl.Message(
    #     content=f"Received: {message.content}",
    # ).send()

    final_answer = await cl.Message(content=f"{message.content}",author="dalong").send()

    # Call the tool
    tool_res = await tool()

    # Send the final answer.
    await cl.Message(content="This is the final answer",author="demo").send()