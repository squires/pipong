import sys
import argparse
import requests
import lirc

host = 'http://localhost:8000/'
lircrc = '/home/pi/pipong/lirc/lircrc-pipong'

def call_endpoint(endpoint):
    url = host + endpoint
    print url
    try:
        response = requests.get(url)
        print response.text
    except Exception as e:
        print(e)

def handle_event(event):
    if event == 'red_up':
        call_endpoint('score/red/up')
    elif event == 'red_down':
        call_endpoint('score/red/down')
    elif event == 'blue_up':
        call_endpoint('score/blue/up')
    elif event == 'blue_down':
        call_endpoint('score/blue/down')
    elif event == 'reset':
        call_endpoint('score/reset')

parser = argparse.ArgumentParser()
parser.add_argument('--url')
parser.add_argument("lirc_config", nargs='?', default=lircrc)
args = parser.parse_args()
if args.url: host = args.url
if args.lirc_config: lircrc = args.lirc_config

try:
    sockid = lirc.init("pipong", lircrc)
    while True:
        event = lirc.nextcode()
        if event:
            handle_event(event.pop())
except (KeyboardInterrupt, SystemExit):
    pipe.close()
    sys.exit(0)

