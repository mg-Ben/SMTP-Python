# SMTP-Python
SMTP mail server connection with Python

# Table of contents
1. [Deploy your local SMTP Server](#deploy-your-local-smtp-server)
2. [Deploy your local SMTP Client](#deploy-your-local-smtp-server)

# Deploy your local SMTP Server
On condition that you want to deploy the SMTP Server:
- Go to /server folder and:

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
3. The ```/src/index.py``` starts running thanks to ```Dockerfile```. [To deploy a SMTP Programmatic Server](https://aiosmtpd.readthedocs.io/en/latest/controller.html) with ```aiosmtpd``` you need to:

    3.1. Create your own Handler class (see ```/src/Handler/HandlerClass.py```) with its constructor. In this HandlerClass.py you can specify which domains your server rely on, or how to handle and print messages.
    
    3.2. Create a Controller object from that HandlerClass:

    ```
    handler = HandlerConstructor()
    controller = Controller(handler, hostname="0.0.0.0") #Please, specify explicitly localhost because otherwise It might use IPv6 default addresses
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

    In short, the complete code looks like this:

    ```
    import Handler.HandlerClass as handler_package
    from aiosmtpd.controller import Controller
    import asyncio

    async def main():
        controller = Controller(handler_package.ExampleHandler(), hostname="0.0.0.0") #Specify custom port if you want (by default = 8025) as port = X, but If you change it, you will need to change it too in docker-compose.yml
        print("Listening...")
        controller.start()
        while True:
            pass

    if __name__ == "__main__":
        asyncio.run(main(), debug=False)
    ```

4. As you are running your SMTP Python server inside a docker container which is running inside your system (host), you need to bind the port of your container to your system port and then you just need to use the system port regardless of the container port. By default, the Python SMTP server runs in 8025 port (you can change it in Controller() and docker-compose.yml). This means that your container is using the 8025 port. Now you have to bind that fixed container port=8025 to the host system port you want. For this purpose, refer to ```docker-compose.yml``` and bind them:

```
ports:
      - ${SMTP_PORT}:8025
```

Where SMTP_PORT is an environment variable you define in ```.env``` file. To sum up: to connect to the server, just use the SMTP_PORT you have set in ```.env``` file.

# Deploy your local SMTP Client

On condition that you want to deploy the SMTP Client:
- Go to /client folder and:

```
docker compose up --build
```

Once you have your server running, you can try to connect to it from a Client Python code just specifying the IP destination and destination port. Since you might be running the server on another host machine and maybe your system hasn't Python installed, the client runs inside another container with its own ```Dockerfile``` and ```docker-compose.yml``` files. However, executing a client inside a container would imply you to bind ports and make some complex configurations and can difficult the task of connecting to remote server by just specifying IP:port to connect to.

For this reason, the client container docker-compose.yml specifies to use the same network as your host machine:

```
network_mode: host
```

Thanks to this configuration, running the python client code container is exactly the same in terms of networking as running in your host machine! So you don't have to specify port binding and, besides, don't need to have installed python because it runs inside a python-based container. All advantages!


# References
[1] [Real Python](https://realpython.com/python-send-email/)