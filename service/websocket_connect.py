import async_timeout
import websockets
import time
import json
import asyncio
jobs = []

async def http_run(connect):
    start = time.time()
    print("Connect websocket {}".format(connect))
    async with websockets.connect("wss://bizapi-staging.hosted.exosite.io/api:1/solution/x9qvfna9tdts0000/logs?token=df5047a5c7b555cf0784591261ab821d413658aa") as websocket:
        resp = await websocket.recv()
        resp_json = json.loads(resp)
        end = time.time()
        print("Wait time: {}".format(end - start))

for i in range(0, 10):
    jobs.append(http_run(i))
    
asyncio.get_event_loop().run_until_complete(asyncio.gather(*jobs))
