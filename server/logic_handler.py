from tornado import gen

class LogicHandler():

    def __init__(self):
        pass

    async def logic_loop(self):
        while True:
            print("Logic coroutine")
            await gen.sleep(1)
