from machine import Pin, I2C
class Sensor():
    def __init__(self):
        self.i2c_temp = I2C(0,scl=Pin(1),sda=Pin(0),freq=400000)
        self.ADDR_temp = 0x44
        #温湿度
        self.i2c_temp.writeto(self.ADDR_temp, b'\x24\x00')
        self.data_temp_hum = self.i2c_temp.readfrom(self.ADDR_temp, 6)
        
    def temp(self):
        temp_raw = self.data_temp_hum[0] << 8 | self.data_temp_hum[1]
        temperature = -45 + 175 * (temp_raw / 65535)
        temp_data=round(temperature,2)
        return temp_data
    def hum(self):
        hum_raw  = self.data_temp_hum[3] << 8 | self.data_temp_hum[4]
        humidity = 100 * (hum_raw / 65535)
        hum_data=round(humidity,2)
        return hum_data
