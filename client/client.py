from smtplib import SMTP as Client

client = Client(host="0.0.0.0", port=8088)
client.sendmail("origin@example.com", ["destination@example.com"],
                "Hello world :D\n")