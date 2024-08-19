from aiohttp import web

from .viewApis import RoutesHandler
from .wsApi import wshandle

# 添加路由: 
def setup_routes(app, rootdir):
    router = app.router
    rh = RoutesHandler(app['config'])
    STATIC_DIR = str(rootdir / 'static')
                      
    routes = [
                web.get('/', rh.indexhandle, name='index'),
                web.get('/ws', wshandle),
                web.get('/testcb', rh.testcb, name='testcb'),
                web.get('/asynctasks', rh.testlooptask, name='asynctasks'),
                web.get('/hello/{name}', rh.indexhandle, name='hello'),
                web.post('/messages', rh.fetch_chat_data, name='aichat'),
                # web.static('/static/', path=STATIC_DIR, show_index=True, name='static')
             ]

    router.add_routes(routes)

# def setup_static_routes(app):
#     app.add_routes([web.static('/static/', path=STATIC_DIR, show_index=True)]) name='static'
