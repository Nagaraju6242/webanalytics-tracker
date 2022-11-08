import random, string
from random import randint, choice
import time
import faker
import os


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


os.environ["TZ"] = "Asia/Kolkata"
fak = faker.Faker()


def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%d/%b/%Y:%I:%M:%S %z", prop)


dictionary = {
    "request": ["GET", "POST", "PUT", "DELETE"],
    "endpoint": [
        "/cart",
        "/cart/add",
        "/order",
        "/cart/checkout",
        "/cart/checkout/confirm",
    ],
    "statuscode": ["303", "404", "500", "403", "502", "304", "200"],
    "username": [
        "james",
        "adam",
        "eve",
        "alex",
        "smith",
        "isabella",
        "david",
        "angela",
        "donald",
        "hilary",
    ],
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "referrer": ["-", fak.uri()],
}


def generate_logs(n):
    f = open("logfiles.log", "w")

    for _ in range(n):
        f.write(
            '%s - - [%s] "%s %s HTTP/1.1" %s %s "-" "%s" \n'
            % (
                fak.ipv4(),
                random_date(
                    "01/Jan/2021:12:00:00 +0530",
                    "01/Jan/2022:12:00:00 +0530",
                    random.random(),
                )[:11]
                + ":12:00:00 +0530",
                choice(dictionary["request"]),
                choice(dictionary["endpoint"]),
                choice(dictionary["statuscode"]),
                str(int(random.gauss(5000, 50))),
                # choice(dictionary["referrer"]),
                dictionary["ua"],
            )
        )

    f.close()


if __name__ == "__main__":
    generate_logs(600)
