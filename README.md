# pipong

pipong is a scoreboard for table tennis that runs on a raspberry pi. It uses an infrared remote control to update the scores. It indicates whose serve it is and recognizes when a game is over.

pipong has been tested on a Raspberry Pi Model B running Raspbian Wheezy with the Epiphany browser (version 3.8.2).

## Design

pipong uses lirc to receive commands from the infrared remote. One python program listens for remote commands and forwards them to a rest api. The second python program hosts the api and serves the scoreboard as a web page. The api/website can be run on the pi itself or out on the network. Anyone who can access the web site can view the scoreboard. The scores are broadcast to all viewers over a websocket.

## Getting Started

### Hardware

  TODO: schematic

  TODO: remote control purchase link (aliexpress 38khz infrared remote control mp3 $0.88)

### Installation

Install lirc:

```
sudo apt-get install lirc liblircclient-dev
```

edit /etc/modules and add the lines:

```
lirc_dev
lirc_rpi gpio_in_pin=0
```

Copy lirc config files:

```
cp lirc/hardware.conf /etc/lirc/hardware.conf
cp lirc/lircd.conf /etc/lirc/lircd.conf
```

Restart lirc:

```
sudo /etc/init.d/lirc restart
```

Install python packages:

Wheezy

```
sudo apt-get install python-lirc python-requests python-flask
pip install gevent gevent-websocket
```

Jessie and newer

```
sudo apt-get install python-lirc python-requests python-flask python-gevent python-gevent-websockets
```

Create named pipe:

```
mkfifo pipong_pipe
```

### Run

Run web server:

```
python web/pipong-web.py
```

Run score event handler:

```
python remote/pipong-remote.py
```

Run irexec:

```
irexec /home/pi/pipong/lircrc
```

