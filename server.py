import asyncio

from aiohttp import web
from concurrent.futures import ThreadPoolExecutor
from run import main as run_main


# 创建线程池
__executor = ThreadPoolExecutor()

# 创建aiohttp应用程序和路由
routes = web.RouteTableDef()


@routes.post('/run')
async def do_run(request):
    # 从请求中获取参数
    args = await request.json()
    try:
        # 使用线程池执行耗时操作
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(__executor, run_main, args)
        # 返回结果
        return web.json_response(result)
    except Exception as e:
        # 返回错误详情
        error_details = {'error': str(e)}
        return web.json_response(error_details, status=500)
