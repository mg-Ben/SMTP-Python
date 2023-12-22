import Handler.HandlerClass as handler_package
from aiosmtpd.controller import Controller
import asyncio

async def main():
    print("Listening...")
    controller = Controller(handler_package.ExampleHandler(), hostname="0.0.0.0")
    controller.start()
    while True:
        pass

if __name__ == "__main__":
    asyncio.run(main(), debug=False)