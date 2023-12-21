# SMTP-Python
SMTP mail server connection with Python

# Table of contents
1. [Deploy your local SMTP server](#deploy-your-local-smtp-server)
On condition that you want to deploy the SMTP server:

```
docker compose up --build
```

### What is happening behind?
1. ```Your docker-compose.yml``` builds the server image from your ```Dockerfile```:

```
python-server:
    build: . (which means "Dockerfile is in the same directory as docker-compose.yml")
```

2. Your ```Dockerfile``` defines how the image is created and what python to run when that image is created (i.e., the main code of your server).
3. The ```src/index.py``` starts running thanks to ```Dockerfile```. [To deploy a SMTP Programmatic Server](https://aiosmtpd.readthedocs.io/en/latest/controller.html) with ```aiosmtpd``` you need to:

    3.1. Create your own Handler class (see ```/src/Handler/HandlerClass.py```) with its constructor.
    
    3.2. Create a Controller object from that HandlerClass:

    ```
    handler = HandlerConstructor()
    controller = Controller(handler)
    ```

    3.3. ```controller.start()``` -> However, It is compulsory to run this line inside an async function (a.k.a. **asynchronous event loop**). Whenever you define an async function in your code and invoke it, you will have to return a promise and so on up to main function. E.g.:

    ```
    async my_function0(){   #1. You define your async function inside which run controller.start()
        ...
        controller.start()  
    }

    async my_function1(){
        await my_function0() #2. You invoke your funcion my_function0, but It is async, so invoke it with await. As my_function0 is async, my_function1 too, so we are forced to define my_function1 as async in the same way.
    }
    
    if __name__="__main__":
        await my_function1() #3. At the end, your main function will also be asynchronous, but this is not possible in Python, as main is not asynchronous!
    ```

    Hence: the solution is ```asyncio``` library, which endows Python with the ability to run, from main, async functions, so [check out this reference](https://docs.python.org/3/library/asyncio-eventloop.html) on how to create an event loop. To work with asynchronous processes in Python, you will need ```asyncio``` library. Luckily, the documentation says...
    
    *Application developers should typically use the high-level asyncio functions, such as asyncio.run(), and should rarely need to reference the loop object or call its methods. This section is intended mostly for authors of lower-level code, libraries, and frameworks, who need finer control over the event loop behavior.*

    Therefore, It's enough with controlling [asyncio Runners](https://docs.python.org/3/library/asyncio-runner.html#asyncio.run), which are coroutines that are executed as event loops (**Watch out! In this context, event loops don't mean processes which are repeatedly such as for or while, but asynchronous tasks!**).

    ```
    async def main():
        ...
        controller.start()

    asyncio.run(main()) #This works!
    ```

4. 

# Deploy your local SMTP server

# References
[1] [Real Python](https://realpython.com/python-send-email/)