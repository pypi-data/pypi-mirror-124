"""
Used to read data and return.
"""
import struct
from datetime import datetime
import time
import calendar

from unisense_xlink.sensors import Bme680Native, Bno055Native, SI1145Native, SI1145NativeRaw
import libscrc


def float_to_serial(float_data: float):
    return struct.pack('f', float_data)


def int_to_serial(int_data: int, signed: bool = False):
    if signed:
        fmt = 'i'
    else:
        fmt = 'I'
    return struct.pack(fmt, int_data)


def time_to_timestamp(dt: datetime):
    time_tuple = dt.utctimetuple()
    time_stamp = calendar.timegm(time_tuple)
    return time_stamp


def ts_to_serial(ts):
    return struct.pack('I', ts)


def time_to_serial(dt: datetime):
    ts = time_to_timestamp(dt)
    return ts_to_serial(ts)


def dsize(bytes_data):
    return struct.calcsize(bytes_data)


def bme_all(as_bytes: bool = False):
    sensor = Bme680Native()
    if as_bytes:
        bytes_data = struct.pack('fff', sensor()[0], sensor()[1], sensor()[2])
        return bytes_data
    return sensor()


def bme_temperature(as_bytes: bool = False):
    """:returns bme680 temperature"""
    data = bme_all()[0]
    if as_bytes:
        return float_to_serial(data)
    return data


def bme_pressure(as_bytes: bool = False):
    """:returns bme680 pressure"""
    data = bme_all()[1]
    if as_bytes:
        return float_to_serial(data)
    return data


def bme_humidity(as_bytes: bool = False):
    """:returns bme680 humidity"""
    data = bme_all()[2]
    if as_bytes:
        return float_to_serial(data)
    return data


def bno_all(as_bytes: bool = False):
    """bno all data has 22 float data which is 22*4 = 88 bytes long.
    so we do not have as_bytes option here."""
    sensor = Bno055Native()
    if as_bytes:
        return struct.pack('H', 255)
    return sensor()


def bno_temperature(as_bytes: bool = False):
    """:returns bno055 temperature"""
    data = bno_all()[0]
    if as_bytes:
        return float_to_serial(data)
    return data


def bno_acceleration(as_bytes: bool = False):
    """:returns bno055 acceleration"""
    data = bno_all()[1]
    if as_bytes:
        return struct.pack('fff', (data[0]), (data[1]), (data[2]))
    return data


def bno_magnetic(as_bytes: bool = False):
    """:returns bno055 magnetic"""
    data = bno_all()[2]
    if as_bytes:
        return struct.pack('fff', data[0], data[1], data[2])
    return data


def bno_gyro(as_bytes: bool = False):
    """:returns bno055 gyro"""
    data = bno_all()[3]
    if as_bytes:
        return struct.pack('fff', data[0], data[1], data[2])
    return data


def bno_euler(as_bytes: bool = False):
    """:returns bno055 euler"""
    data = bno_all()[4]
    if as_bytes:
        return struct.pack('fff', data[0], data[1], data[2])
    return data


def bno_quaternion(as_bytes: bool = False):
    """:returns bno055 quaternion"""
    data = bno_all()[5]
    if as_bytes:
        return struct.pack('fff', data[0], data[1], data[2])
    return data


def bno_linear_acceleration(as_bytes: bool = False):
    """:returns bno055 linear_acceleration"""
    data = bno_all()[6]
    if as_bytes:
        return struct.pack('fff', data[0], data[1], data[2])
    return data


def bno_gravity(as_bytes: bool = False):
    """:returns bno055 gravity"""
    data = bno_all()[7]
    if as_bytes:
        return struct.pack('fff', data[0], data[1], data[2])
    return data


def si_all(with_exceptions: bool = False, as_bytes: bool = False):
    """:returns all si data vis:ir:uv"""
    if with_exceptions:
        sensor = SI1145NativeRaw()
    else:
        sensor = SI1145Native()
    if as_bytes:
        bytes_data = struct.pack('IIH', sensor()[0], sensor()[1], sensor()[2])
        return bytes_data
    return sensor()


def si_vis(with_exceptions: bool = False, as_bytes: bool = False):
    """si1145:vis"""
    if with_exceptions:
        data = si_all(with_exceptions=True)[0]
    else:
        data = si_all()[0]
    if as_bytes:
        return struct.pack('I', data)
    return data


def si_ir(with_exceptions: bool = False, as_bytes: bool = False):
    """si1145:ir"""
    if with_exceptions:
        data = si_all(with_exceptions=True)[1]
    else:
        data = si_all()[1]
    if as_bytes:
        return struct.pack('I', data)
    return data


def si_uv(with_exceptions: bool = False, as_bytes: bool = False):
    """si1145:uv"""
    if with_exceptions:
        data = si_all(with_exceptions=True)[2]
    else:
        data = si_all()[2]
    if as_bytes:
        return struct.pack('H', data)
    return data


def repr_hex(bytes_obj: bytes):
    return bytes_obj.hex()


def calc_crc(data, return_type: str = 'hex'):
    """ returns little endian modbus crc16
    :param data bytes data
    :param return_type str hex,bytes
    :return crc16 modbus
    """
    res = struct.pack('h', libscrc.modbus(data))
    if return_type == 'bytes':
        return res
    return res.hex()
