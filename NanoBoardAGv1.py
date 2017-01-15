import serial
import time
import struct


# Linux
# ser = serial.Serial("/dev/ttyUSB0",38400)

# Mac OS X
# ser = serial.Serial("/dev/tty.usbserial", 38400)


class NanoBoardAG():
    def __init__(self):
        self.valResistanceD = float()
        self.valResistanceC = float()
        self.valResistanceB = float()
        self.valButton = float()
        self.valResistanceA = float()
        self.valLight = float()
        self.valSound = float()
        self.valSlider = float()
        self.is_motor_on = False
        self.motorDirection = 0
        self.motorPower = 100
        self.ser = serial.Serial("/dev/cu.usbserial", 38400, timeout=1)
        # 起動待ち
        time.sleep(1.8)
        self.in_bytes = [0]*18

    def set_value(self, in_bytes):
        self.valResistanceD = ((in_bytes[2] & 0x07) * 128 + in_bytes[3]) * 100 / 1023.0
        self.valResistanceC = ((in_bytes[4] & 0x07) * 128 + in_bytes[5]) * 100 / 1023.0
        self.valResistanceB = ((in_bytes[6] & 0x07) * 128 + in_bytes[7]) * 100 / 1023.0
        self.valButton = 100 - ((in_bytes[8] & 0x07) * 128 + in_bytes[9]) * 100 / 1023.0
        self.valResistanceA = ((in_bytes[10] & 0x07) * 128 + in_bytes[11]) * 100 / 1023.0
        self.valLight = 100 - ((in_bytes[12] & 0x07) * 128 + in_bytes[13]) * 100 / 1023.0
        self.valSound = ((in_bytes[14] & 0x07) * 128 + in_bytes[15]) * 100 / 1023.0
        self.valSlider = ((in_bytes[16] & 0x07) * 128 + in_bytes[17]) * 100 / 1023.0
        print('Light is ', end='')
        print(self.valLight, end='')
        print('     Button is ', end='')
        print(self.valButton, end='')
        print('     Slide is ', end='')
        print(self.valSlider)

    def run(self):
        if self.is_motor_on:
            self.send_data()
        else:
            self.ser.write(b'\x00')
        temp = self.ser.read(18)
        self.in_bytes = struct.unpack('18B', temp)
        print(self.in_bytes)
        self.set_value(self.in_bytes)

    def set_motor_power(self, power):
        self.motorPower = int(power * 1.28)

    def reverse_motor_direction(self):
        self.motorDirection = (self.motorDirection + 1) & 0x1

    def send_data(self):
        self.ser.write((self.motorDirection << 7 | self.motorPower).to_bytes(1, 'big'))

if __name__ == '__main__':
    # root = tk.Tk()
    # root.title()
    # root.configure(width = 640, height=480)
    nano = NanoBoardAG()
    nano.run()
    time.sleep(2)
    nano.reverse_motor_direction()
    nano.set_motor_power(50)
    nano.is_motor_on = True
    # nano.reverse_motor_direction()
    nano.run()
    time.sleep(3)
    nano.is_motor_on = False
    nano.run()

    # root.mainloop()