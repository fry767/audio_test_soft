import sys
import usb
import usb.core
import usb.util


def get_available_serial():
    devs = usb.core.find(find_all=True)
    available_serial = []
    for dev in devs:
        if dev.iSerialNumber != 0:
            product = dev.product
            if product == 'EVK1.4':
                serial = usb.util.get_string(dev,dev.iSerialNumber,None)
                available_serial.append(serial)
    return available_serial
