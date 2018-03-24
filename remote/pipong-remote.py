import sys
import requests

#if len(sys.argv) <= 1:
#    sys.exit(0)

#event = sys.argv[1]
#print event

host = 'http://localhost:8000/'

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

# open the pipe for reading and writing so that at
# least one process (us) always has it open for writing
# so that we don't receive an EOF after each message
pipe = open('/home/pi/pipong/pipong_pipe', 'w+')

try:
    while True:
        event = pipe.readline()
        print 'event: ' + event.strip()
        if len(event) > 0:
            handle_event(event.strip())
except (KeyboardInterrupt, SystemExit):
    pipe.close()
    sys.exit(0)

