# bme680 import
import bme680

# bno055 imports
import adafruit_bno055
import board
# SI1145 imports
import SI1145.SI1145 as SI1145

i2c = board.I2C()


class Bme680Native:
    """'temperature,pressure,humidity'"""

    def __init__(self) -> None:
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)

        self.temperature = self.sensor.data.temperature
        self.pressure = self.sensor.data.pressure
        self.humidity = self.sensor.data.humidity

    def __call__(self, *args, **kwargs):
        return self.temperature, self.pressure, self.humidity


class Bno055Native:
    """Returns data;
    self.temperature,  float
    self.acceleration,   (float,float,float)
    self.magnetic,   (float,float,float)
    self.gyro,    (float,float,float)
    self.euler,   (float,float,float)
    self.quaternion,    (float,float,float)
    self.linear_acceleration,    (float,float,float)
    self.gravity    (float,float,float)
    """

    def __init__(self):
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        self.temperature = self.sensor.temperature
        self.acceleration = self.sensor.acceleration
        self.magnetic = self.sensor.magnetic
        self.gyro = self.sensor.gyro
        self.euler = self.sensor.euler
        self.quaternion = self.sensor.quaternion
        self.linear_acceleration = self.sensor.linear_acceleration
        self.gravity = self.sensor.gravity

    def __call__(self, *args, **kwargs):
        return (self.temperature,
                self.acceleration,
                self.magnetic,
                self.gyro,
                self.euler,
                self.quaternion,
                self.linear_acceleration,
                self.gravity
                )


class SI1145Native:
    """vis,ir,uv : int, int ,short [I,I,H]"""

    def __init__(self):
        self.sensor = SI1145.SI1145()
        try:
            self.vis = self.sensor.readVisible()
        except:
            self.vis = 0

        try:
            self.ir = self.sensor.readIR()
        except:
            self.ir = 0

        try:
            self.uv = self.sensor.readUV()
        except:
            self.uv = 0

    def __call__(self, *args, **kwargs):
        return (self.vis,
                self.ir,
                self.uv
                )


class SI1145NativeRaw:
    """vis,ir,uv : int, int ,short [I,I,H]"""

    def __init__(self):
        self.sensor = SI1145.SI1145()
        self.vis = self.sensor.readVisible()
        self.ir = self.sensor.readIR()
        self.uv = self.sensor.readUV()

    def __call__(self, *args, **kwargs):
        return (self.vis,
                self.ir,
                self.uv
                )
