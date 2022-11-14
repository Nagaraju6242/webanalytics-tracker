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


def get_frontend_snippet(trackId):
    FRONTEND_JS_SNIPPET = (
        '<script>const track_url="http://127.0.0.1:8000/api/track/",trackId="'
        + trackId
        + '",trackable_events_url=`http://127.0.0.1:8000/api/trackable_events/${trackId}/`;var scrolled=!0,head=document.getElementsByTagName("head")[0],script=document.createElement("script");async function sendData(e){return e.origin=location.origin,e.trackId=trackId,config={method:"POST",body:JSON.stringify(e)},res=await fetch(track_url,e=config),await res.json()}async function handler(){pageLoadData={eventType:"pageview",eventName:document.title},sendData(pageLoadData),trackable_events=await get_trackable_events(),add_event_listeners(trackable_events)}async function get_trackable_events(){return response=await fetch(trackable_events_url),data=await response.json(),"ok"==data.status?data.data:null}function add_event_listeners(e){e.forEach((e=>{"click"==e.type&&(selector="",e.html_selector?selector=e.html_selector:(e.html_tag&&(selector+=e.html_tag),e.html_id&&(selector+=`#${e.html_id}`),e.html_class&&(selector+=`.${e.html_class}`)),$(selector).on("click",(function(t){t.preventDefault(),clickData={eventType:"click",eventName:e.name},sendData(clickData)})))})),window.onscroll=function(){scrollData={eventType:"scroll",eventName:document.title},scrolled&&(sendData(scrollData),scrolled=!1,setTimeout((function(){scrolled=!0}),5e3))}}script.type="text/javascript",script.src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.1/jquery.min.js",script.onreadystatechange=handler,script.onload=handler,head.appendChild(script);</script>'
    )
    return FRONTEND_JS_SNIPPET


if __name__ == "__main__":
    # generate_logs(600)
    print(get_frontend_snippet("LOD9755CQT"))
