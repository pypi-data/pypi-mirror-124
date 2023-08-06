import json
import logging
import time
import socket
import os.path
import re
import uuid
from threading import Timer
from typing import Callable

from paho.mqtt import client as mqtt_client

import yaml
from yaml.error import YAMLError


logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="[%H:%M:%S]", level=logging.DEBUG
)


class RepeatTimer:
    """The class is used to repeat a task.

    Attributes:
        timeout (int): How often the timer is repeated
        func (Callable): The function to repeat
        thread (Timer): The thread running the timer


    Args:
        timeout (int): How often the timer is repeated
        func (Callable): The function to repeat
    """

    def __init__(self, timeout: int, func: Callable):
        self.timeout = timeout
        self.func = func
        self.thread = Timer(self.timeout, self.handle_function)

    def handle_function(self):
        """Executes the function, and restart the timer"""
        self.func()
        self.thread = Timer(self.timeout, self.handle_function)
        self.thread.start()

    def start(self):
        """Starts the timer for the first time"""
        self.thread.start()


class BasicDyrkDevice:
    """The basicdyrkdevice object implements a basic structure for a dyrk device.
    The dyrk device reads a yaml config file which defaults to the path "deviceconfig.yml".
    After starting the object, it will connect via MQTT and run the decorated functions in response to events happening,
    with the option of adding custom event types.
    In addition, it supports measurements by repeating a function with an interval and sending the data via MQQT.

    A basic usage of this is::

        from dyrkdevice.basicDyrkDevice import BasicDyrkDevice

        device = BasicDyrkDevice()

        # reacts to the event with name "output_event"
        @device.event(eventName="output_event")
        def output(output_state: list):
            print("output event invoked")

        # Adds metadata fields to the returned dictionary and
        # sends it via mqqt every 10 second
        @device.measure(measureName="fakeMeasure", interval=10)
        def fake():
            return {
                "temperature": 22,
                "pressure": 1000,
                "humidity": 55,
            }

        # In case of custom events or overwriting of behavior
        @device.eventParser(eventName="customEvent")
        def customEventParser(self, event: dict):
            return event["customField"]

        @device.event(eventName="customEvent")
        def custom(customField: str):
            print("custom event invoked")


        device.run()
    """

    def __init__(self, config: str = "deviceconfig.yml"):
        self.EVENTS = dict()
        self.MEASURES = dict()
        self.EVENTPARSERS = dict()

        self.EVENTPARSERS["enroll_event"] = self.enrollEventParser
        self.EVENTPARSERS["output_event"] = self.outputEventParser
        self.EVENTPARSERS["data_event"] = self.dataEventParser

        self.EVENTS["enroll_event"] = self._subscribe_to_topic

        self._loadConfig(config)

    def _loadConfig(self, config: str):
        """Tests if a config file exists and loads it.
        If it does not exist it creates a template and exits.

        Args:
            config (str): Path to configfile
        """

        if not os.path.isfile(config):
            self._generateConfig(config)

        with open(config, encoding="utf-8") as file:
            try:
                self.config = yaml.load(file, Loader=yaml.FullLoader)
            except YAMLError as exc:
                if exc.context is not None:
                    logging.error(
                        "Failed to parse yaml file with error:\n"
                        + str(exc.problem_mark)
                        + "\n  "
                        + str(exc.problem)
                        + " "
                        + str(exc.context)
                    )
                else:
                    logging.error("Failed to parse yaml file, with no further details")
                exit()

        self._validateConfig()

        return

    def _validateConfig(self) -> bool:
        """Validates the currently loaded configuration

        Returns:
            bool: [description]
        """

        ##### validates the expected keys are present
        if "mqtt" not in self.config.keys():
            logging.error("Configuration is missing section: mqtt")
            exit()
        if "broker" not in self.config["mqtt"].keys():
            logging.error("Configuration is missing section: mqtt.broker")
            exit()

        mqttBrokerSectionReq = ("endpoint", "port", "client_id", "username", "password")
        if not all(
            key in self.config["mqtt"]["broker"] for key in mqttBrokerSectionReq
        ):
            logging.error(
                "Configuration is section is incomplete: mqtt.broker\n"
                + f"Section had attributes {self.config['mqtt']['broker'].keys()}, expected {mqttBrokerSectionReq}"
            )
            exit()

        ##### validate the hostname
        hostname = self.config["mqtt"]["broker"]["endpoint"]
        if not hostname:
            logging.error("Hostname is empty")
            exit()
        if len(hostname) > 255:
            logging.error(
                "Hostname is too long, a hostnaem must be below 255 characters"
            )
            exit()
        if hostname[-1] == ".":
            hostname = hostname[:-1]  # strip exactly one dot from the right, if present
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        if not all(allowed.match(x) for x in hostname.split(".")):
            logging.error(f"Hostname has illigal characters. Hostname was {hostname}")
            exit()

        #### validate port number is sane
        port = self.config["mqtt"]["broker"]["port"]
        if (port < 0) or (port > 655535):
            logging.error(f"Port number not in 0-65535 range, port was {port}")
            exit()

        # validates if deviceid

    def _getMac(self) -> str:
        """Returns the mac adress

        Returns:
            str: mac adress E.G 00:16:3e:99:0b:db
        """
        return ":".join(re.findall("..", "%012x" % uuid.getnode()))

    def _generateConfig(self, path: str):
        """Generates a configuration template and writes it to a file

        Args:
            path (str): Path to output the yaml file
        """
        config = {"mqtt": {"broker": {}}}
        config["mqtt"]["broker"]["endpoint"] = ""
        config["mqtt"]["broker"]["port"] = 1883
        config["mqtt"]["broker"]["client_id"] = f"dyrk_DEVICE_{self._getMac()[-5:]}"
        config["mqtt"]["broker"]["username"] = ""
        config["mqtt"]["broker"]["password"] = ""

        with open(path, encoding="utf-8", mode="w") as file:
            yaml.dump(config, file)

    def _ping(self, endpoint: str, port: int) -> bool:
        """Returns true if pingable, false if not

        Args:
            endpoint (str): The IP or endpoint to try
            port (str): The port to test

        Returns:
            bool: True if succesfull, otherwise False
        """
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if a_socket.connect_ex((endpoint, port)):
            return False

        return True

    def connect_mqtt(self) -> mqtt_client:
        """Connects to the mqtt server with the info from the deviceconfiguration

        Returns:
            mqtt_client: A connected mqtt client
        """

        broker = self.config["mqtt"]["broker"]["endpoint"]
        port = self.config["mqtt"]["broker"]["port"]
        # generate client ID with pub prefix randomly
        client_id = self.config["mqtt"]["broker"]["client_id"]
        username = self.config["mqtt"]["broker"]["username"]
        password = self.config["mqtt"]["broker"]["password"]

        def _on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT Broker!")
            else:
                logging.info("Failed to connect, return code %d\n", rc)

        # Set Connecting Client ID
        while not self._ping(broker, port):
            logging.info(
                f"Cannot ping endpoint {broker}:{port}, retrying in 30 seconds"
            )
            time.sleep(30)

        client = mqtt_client.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = _on_connect
        client.connect(broker, port)

        return client

    def _subscribe_to_topic(self, topic: str):
        """Subscribes to a topic on the MQQT client

        Args:
            topic (str): The topic to subscribe
        """

        logging.info(f"Subscribing to topic: {topic}")

        def _on_message(msg):
            try:
                eventstring = msg.payload.decode()
                parsedevent = json.loads(eventstring)
                logging.info(f"[{msg.topic}] Received an event: {parsedevent}")
                if parsedevent["event_type"] not in self.EVENTS.keys():
                    logging.info("Event unsupported")
                    return
                if parsedevent["event_type"] not in self.EVENTPARSERS.keys():
                    logging.info("Event unsupported")
                    return

                self.EVENTS[parsedevent["event_type"]](
                    self.EVENTPARSERS[parsedevent["event_type"]](parsedevent)
                )

            except ValueError:
                logging.info("String could not be converted to JSON.")

        self.client.subscribe(topic)
        self.client.on_message = _on_message
        return

    def outputEventParser(self, event: dict):
        return event["output_amount"]

    def enrollEventParser(self, event: dict):
        return event["plan_id"]

    def dataEventParser(self, event: dict):
        return

    def event(self, eventName: str):
        """A decorator adding a function handler to a event.

        Args:
            eventName (str): The name of the event for which to use the function
        """

        def eventdecorator(func):
            self.EVENTS[eventName] = func
            return func

        return eventdecorator

    def eventParser(self, eventName: str):
        def parserdecorator(func):
            self.EVENTPARSERS[eventName] = func
            return func

        return parserdecorator

    def measure(self, measureName: str, interval: int):
        """Sends a dictionary with some added metadata on the devices data chennel at an interval.

        Args:
            measureName (str): The name of the measurement E.G dht11
            interval (int): The interval to run the measurement in seconds
        """

        def decorator(func):
            def send_dict():
                data = func()

                data["event_type"] = "data_event"
                data["timestamp"] = int(time.time())

                eventstring = json.dumps(data)
                self.client.publish(self.data_channel_id, eventstring)

            timer = RepeatTimer(interval, send_dict)
            self.MEASURES[measureName] = timer
            return timer

        return decorator

    def run(self):
        """Starts the object by connecting to the MQQT broker and starting the timed measurements"""
        self.command_channel_id = (
            self.config["mqtt"]["broker"]["client_id"] + "_command"
        )
        self.data_channel_id = self.config["mqtt"]["broker"]["client_id"] + "_data"

        self.client = self.connect_mqtt()
        self._subscribe_to_topic(self.command_channel_id)
        self._subscribe_to_topic(self.data_channel_id)

        for name, thread in self.MEASURES.items():
            thread.start()
            logging.info(f"started {name}")

        self.client.loop_start()
        while True:
            pass
