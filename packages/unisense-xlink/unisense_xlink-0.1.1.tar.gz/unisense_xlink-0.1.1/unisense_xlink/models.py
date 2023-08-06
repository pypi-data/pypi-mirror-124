# python core imports
from typing import Tuple
from datetime import datetime
# pydantic imports
from pydantic import BaseModel

from unisense_xlink import core
from unisense_xlink.core import time_to_serial

"""
Data Length

temperature: int 4
float : 4
"""


class BmeDataBase(BaseModel):
    temperature: float = core.bme_temperature()
    pressure: float = core.bme_pressure()
    humidity: float = core.bme_humidity()


class BmeDataBaseTime(BmeDataBase):
    updated: datetime = datetime.utcnow()


class BmeDataBin(BaseModel):
    temperature: bytes = core.bme_temperature(as_bytes=True)
    pressure: bytes = core.bme_pressure(as_bytes=True)
    humidity: bytes = core.bme_humidity(as_bytes=True)


class BmeDataAll(BaseModel):
    data: bytes = core.bme_all(as_bytes=True)


class BmeDataBinTime(BmeDataBin):
    updated: bytes = time_to_serial(datetime.utcnow())


class BnoDataBase(BaseModel):
    temperature: float = core.bno_temperature()
    acceleration: Tuple[float, float, float] = core.bno_acceleration()
    magnetic: Tuple[float, float, float] = core.bno_magnetic()
    gyro: Tuple[float, float, float] = core.bno_gyro()
    euler: Tuple[float, float, float] = core.bno_euler()
    quaternion: Tuple[float, float, float] = core.bno_quaternion()
    linear_acceleration: Tuple[float, float, float] = core.bno_linear_acceleration()
    gravity: Tuple[float, float, float] = core.bno_gravity()


class BnoDataBaseTime(BnoDataBase):
    updated: datetime = datetime.utcnow()


class BnoDataBin(BaseModel):
    temperature: bytes = core.bno_temperature(as_bytes=True)
    acceleration: bytes = core.bno_acceleration(as_bytes=True)
    magnetic: bytes = core.bno_magnetic(as_bytes=True)
    gyro: bytes = core.bno_gyro(as_bytes=True)
    euler: bytes = core.bno_euler(as_bytes=True)
    quaternion: bytes = core.bno_quaternion(as_bytes=True)
    linear_acceleration: bytes = core.bno_linear_acceleration(as_bytes=True)
    gravity: bytes = core.bno_gravity(as_bytes=True)


class BnoDataBinTime(BnoDataBin):
    updated: bytes = time_to_serial(datetime.utcnow())


class SiDataBase(BaseModel):
    vis: int = core.si_vis()
    ir: int = core.si_ir()
    uv: int = core.si_uv()


class SiDataBaseException(BaseModel):
    vis: int = core.si_vis(with_exceptions=True)
    ir: int = core.si_ir(with_exceptions=True)
    uv: int = core.si_uv(with_exceptions=True)


class SiDataBaseTime(SiDataBase):
    updated: datetime = datetime.utcnow()


class SiDataBaseExceptionTime(SiDataBaseException):
    updated: datetime = datetime.utcnow()


class SiDataBin(BaseModel):
    vis: bytes = core.si_vis(with_exceptions=False, as_bytes=True)
    ir: bytes = core.si_ir(with_exceptions=False, as_bytes=True)
    uv: bytes = core.si_uv(with_exceptions=False, as_bytes=True)


class SiDataAll(BaseModel):
    data: bytes = core.si_all(as_bytes=True)


class SiDataBinTime(SiDataBin):
    updated: bytes = time_to_serial(datetime.utcnow())
