# pipong

pipong is a scoreboard for table tennis that runs on a Raspberry Pi. It uses an infrared remote control to update the scores. It indicates whose serve it is and recognizes when a game is over.

pipong has been tested on a Raspberry Pi Model B running Raspbian Wheezy with the Epiphany browser (version 3.8.2).

![Screenshot](doc/screenshot.png)

## Design

pipong uses lirc to receive commands from the infrared remote. One python program listens for remote commands and forwards them to a rest api. The second python program hosts the api and serves the scoreboard as a web page. The api/website can be run on the pi itself or out on the network. Anyone who can access the web site can view the scoreboard. The scores are broadcast to all viewers over a websocket.

## Getting Started

### Hardware

This is the particular remote that this project is configured for by default. It is available at AliExpress (for example, at the time of this writing, [38kHz "Car MP3" Remote Control](https://www.aliexpress.com/item/1pcs-lot-38khz-MCU-learning-board-IR-remote-control-Infrared-decoder-for-protocol-remote-control-For/32711105886.html)). If you use a different remote, you'll need to train lirc to use it.

![IR Remote Control](doc/remote-annotated.jpg)

I used a Vishay TSOP38338 sensor, with the following schematic. It should work without the resistor and capacitor, but the datasheet recommends them.

![Schematic](doc/schematic.png)

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

### Run

Run web server:

```
python web/pipong-web.py
```

Run remote interface:

```
python remote/pipong-remote.py
```

Open browser to ```http://localhost:8000```.

### Sys V Init Scripts

My Pi is still running Wheezy, so it uses init.d for starting services.

Copy init scripts to /etc/init.d:

```
sudo cp initd/pipong-remote /etc/init.d
sudo cp initd/pipong-web /etc/init.d
```

Update init script links:

```
sudo update-rc.d pipong-remote defaults
sudo update-rc.d pipong-web defaults
```

