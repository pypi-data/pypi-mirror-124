# Dyrk Device
This library helps implement a dyrk device in the ecosystem of dyrk.io

The library takes care of connection and communication with the dyrk host, and leaves the implementation of the functions to the user

## Getting started

### Installing
```
$ pip install dyrkdevice
```

### implementing a device
```
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
```

