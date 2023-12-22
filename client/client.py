from smtplib import SMTP as Client

client = Client(host="0.0.0.0", port=8088)
client.sendmail("origin@gmail.com", ["benjaminmartin1008@gmail.com"],
                "Hello world :D\n")