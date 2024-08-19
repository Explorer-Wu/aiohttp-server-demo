#!/usr/bin/python3 
#coding=utf-8
import asyncio
from aiohttp import web
from langchain_openai import ChatOpenAI
import json
import logging
import pathlib

from service.routes import setup_routes
from config.settings import get_config
from tools.utils import on_shutdown

# 配置日志
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s line:%(lineno)d %(filename)s %(funcName)s >>> %(message)s')

# import aiohttp_jinja2, jinja2


global_conf = None

# pathlib.Path(__file__).parent
BASE_ROOT = pathlib.Path(__file__)

def init_app():
	# __name__表示当前的模块名称
	app = web.Application()
	app['config'] = get_config()
	# 加载模板
	# aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('www', 'templates'))
	# 程序启动和关闭的回调函数
	# app.on_startup.append(init_db)
	# app.on_cleanup.append(close_db)
	app.on_cleanup.append(on_shutdown)
	# 添加中间件
	# set_middleware(app)

	# 设置websockets
	app['websockets'] = {}
	# 设置路由
	setup_routes(app, BASE_ROOT)

	# global global_conf
	# global_conf = get_config()
	host, port = app['config']['server']['host'], app['config']['server']['port']
  
	return app, host, port


async def get_app():
    """Used by aiohttp-devtools for local development."""
    import aiohttp_debugtoolbar
    app, _, _ = await init_app()
    aiohttp_debugtoolbar.setup(app)
    return app


def main():
	logging.basicConfig(level=logging.DEBUG)
	# 创建并返回一个新的事件循环对象
	# loop = asyncio.new_event_loop()
	# 将 loop 设为当前 OS 线程的当前事件循环
	# asyncio.set_event_loop(loop)
	# init_task = asyncio.create_task(init_app())
	# run_until_complete(future) 运行直到 future 实例被完成
	app, host, port = init_app() 
	# loop.run_until_complete(init_task)
	# 启动程序
	web.run_app(app, host=host, port=port)

		# Debug/Development  app.run() 默认5000
		# app.run(debug=True, host='0.0.0.0', port=5001)

# __name__ 参数是特殊的Python变量，当脚本被执行时，它的值为'__main__'，这个条件语句保证应用程序只在被作为主程序运行时才会执行
if __name__ == '__main__':
	main()
	# Production
	# from gevent.pywsgi import WSGIServer
	# http_server = WSGIServer(('', 5000), app)
	# http_server.serve_forever()


