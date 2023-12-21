from Handler.HandlerClass import ExampleHandler
from aiosmtpd.controller import Controller
import asyncio

async def main():
    controller = Controller(ExampleHandler())
    print("Listening...")
    controller.start()
    while True:
        pass

if __name__ == "__main__":
    asyncio.run(main(), debug=False)