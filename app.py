import asyncio

import itertools

import json


import websockets


#from video import Imagedetection

async def handler(websocket):

    # Initialize detection
    #detect =Imagedetection()

    #if detect.fruit is not None:
        #event = {

                #"event": "detected",

                #"fruit": detect.fruit,

        #}
        #print(event)
        await websocket.send()




async def main():

    async with websockets.serve(handler, "localhost", 8001):

        await asyncio.Future()  # run forever



if __name__ == "__main__":

    asyncio.run(main())