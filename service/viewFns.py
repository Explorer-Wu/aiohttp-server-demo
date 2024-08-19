import asyncio
from aiohttp import web, ClientSession
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# import getpass
# import os

# os.environ["OPENAI_API_KEY"] = getpass.getpass()


async def say_hello(name):
    await asyncio.sleep(1)
    return "Hello, " + name


# 使用回调函数
def async_task(callback):
    asyncio.create_task(async_task_impl(callback))

async def async_task_impl(callback):
    await asyncio.sleep(1)
    result = "Hello, Waiting for me"
    callback(result)


# 用在客户端，服务端不可用
async def fetch(url):
    async with ClientSession() as session:
    # await表示阻塞挂起
        try:
            # session.get(url, proxy=proxy)
            async with session.get(url) as response:
                return await response.text()
        except Exception as e:
            print('Error：', e.args)


async def async_url_join(url):
    await asyncio.sleep(1)
    result = "Hello, " + url
    return result



# openai_apikey = global_conf['llms']['openai_apikey']

async def do_llm_data(reqdata, apikey):

    llmGpt = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=apikey,  # if you prefer to pass api key in directly instaed of using env vars
        # base_url="...",
        # organization="...",
        # other params...
    )
    # resdata = {
    #     "code": 'success',
    #     "data": {
    #         "model": reqdata.get('model'),
    #         "chatmsg": '我收到消息，认真解答中...'
    #     }
    # }
    resdata = await llmGpt.invoke([HumanMessage(content=reqdata.msg)])
    logging.info('响应数据：', str(resdata))
    return resdata
