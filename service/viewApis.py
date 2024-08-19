import asyncio
from aiohttp import web
import logging
import datetime
import time
import threading

from .viewFns import say_hello, async_task, async_url_join, fetch, do_llm_data

class RoutesHandler:

    def __init__(self, config):
        self.config = config
        # pass

    # 定义url请求路径
    async def indexhandle(self, request):
        """定义视图函数"""
        # 默认值 "Anonymous"
        name = request.match_info.get('name', "Anonymous")
        logging.info('首页：', name)

        result = await say_hello(name)
        # txt = "Hello, {}".format(name)
        text = f"<h1>{result}</h1>"
        # return web.Response(text=text) 加 content_type="text/html" 识别html
        return web.Response(text=text, content_type="text/html")

    async def testcb(self, request):
        # name = request.match_info.get('name', "Anonymous")
        def calltest(result):
            return result

        async_task(calltest)
        ntext = "Waiting for ..."
        
        response = await fetch('https://www.sina.com.cn/api/hotword.json')
        # print(f"testcb数据： {response}")
        return web.Response(text=ntext+response, content_type="text/html")

    async def testlooptask(self, request):
        async def do_async_tasks():
            urls = [
                "https://www.sina.com.cn/api/hotword.json",
                "https://odin.sohu.com/odin/api/blockdata",
                "https://photo.home.163.com/api/designer/pc/home/index/word"
            ]
            # 准备一个tasks数组
            ntasks = []
            # 对协程对象进行封装为task
            ntasks = [asyncio.create_task(fetch(url)) for url in urls]
            # for url in urls:
            #     # cop = await async_url_join(url) 
            #     task = asyncio.create_task(fetch(url))
            #     ntasks.append(task)
            
            try:
                done, pending = await asyncio.wait(ntasks, timeout=5)
                print("asynctasks数据:", done)
            except asyncio.TimeoutError:
                print("超时啦")
                # 任务被取消：返回 True，没有被取消：返回 False
                for task in pending:
                    task.cancel()
                    print(f"任务 {task} 是否被取消: {task.cancelled()}")
            
            # return done
            # 得到执行结果
            for do in done:
                res = do.result()
                print(f"{time.time()} 得到执行结果: {res}")


        # 计时
        start = time.time()
        # 把异步方法注册到事件循环中
        # loop = asyncio.get_event_loop()
        loop = asyncio.get_event_loop()
        if loop.is_running():
            def create_loop():
                loop = asyncio.new_event_loop
                asyncio.set_event_loop(loop)
                print("重制事件循环loop:", loop)

                try:
                    loop.run_until_complete(do_async_tasks())
                finally:
                    loop.close()

            threading.Thread(target=create_loop).start()
        else:
            print("正运行的事件循环loop:", loop)

        loop.run_until_complete(do_async_tasks())
        end = time.time()
        total_time = end - start
        logging.info('总耗时:', total_time)
        

        return web.Response(text='total_time')
        

    async def fetch_chat_data(self, request: web.Request) -> web.Response:
        try:
            raw_data = await request.post()
            # post = await request.json()
            
            # raw_data = form['file'].file.read()
            # form["file"].file.close()
            # executor = request.app['executor']
            # raw_data = await r(executor, predict, raw_data)
            # raw_data = predict(raw_data)
        
            # 如果得到的data是字符串格式，则需要用json.loads来变换成python格式，看个人需求
            # data = json.loads(data)
            # print(data)
            logging.info('请求数据：', raw_data)
            # 获取 POST 请求中的 JSON 数据
        except Exception as e:
            return jsonify({'error': '请求数据失败'}), 400

        # 处理数据
        # 调用do_process_data函数来处理接收到的数据。
        # 判断是否接收到数据
        if raw_data:
            try:
                res_data = await do_llm_data(raw_data, self.config['llms']['openai_apikey'])
                headers = {'Content-Type': 'application/json'}
            except Exception as e:
                return jsonify({'error': '处理数据失败'})

            # 返回的数据格式看请求方的要求了，也有可能需要json处理后的数据，即jsonify(processed_data)
            return web.Response(body=res_data, headers=headers)
            # return jsonify(processed_data)