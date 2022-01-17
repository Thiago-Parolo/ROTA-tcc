from machine import Pin, PWM
import uasyncio as asyncio

from ble import BLE

class ESPControll:
    def __init__(self, _servo, _motorA, _motorB, _speed, angle):
        servo_pin = Pin(_servo, Pin.OUT)
        self.servo = PWM(servo_pin, freq=50, duty=angle)

        self.motor_pin_A = Pin(_motorA, Pin.OUT)
        self.motor_pin_B = Pin(_motorB, Pin.OUT)

        self.speed_pin = Pin(_speed, Pin.OUT)
        self.speed = PWM(self.speed_pin, freq=100, duty=0)
        self.current_speed = 512

        self.ble = BLE("rota")
        self.angle = angle

    def set_speed(self, speed):
        self.speed.duty(speed)

    async def walk(self):
        while self.current_speed > 0:
            self.set_speed(self.current_speed - 16)
            await asyncio.sleep_ms(10)

        self.motorB.value(0)
        self.motorA.value(1)
        
        while self.current_speed < 512:
            self.set_speed(self.current_speed + 16)
            await asyncio.sleep_ms(10)

    async def turn_right(self):
        if (self.angle >= 105):
            return
        
        self.servo.duty(self.angle + 28)
        self.angle += 28

    async def reverse(self):
        while self.current_speed > 0:
            self.set_speed(self.current_speed - 16)
            await asyncio.sleep_ms(10)

        self.motorA.value(0)
        self.motorB.value(1)
        
        while self.current_speed < 512:
            self.set_speed(self.current_speed + 16)
            await asyncio.sleep_ms(10)

    async def turn_left(self):
        if (self.angle <= 50):
            return
        
        self.servo.duty(self.angle - 28)
        self.angle -= 28

    async def stop(self):
        while self.current_speed > 0:
            self.set_speed(self.current_speed - 16)
            await asyncio.sleep_ms(10)
            
        self.motorA.value(0)
        self.motorB.value(0)

    async def honk():
        notes = [783,783,783,523,659,783,783,783,523,659,523,523,987,987,880,880,783]
        tempo = [200, 200, 200, 400, 500, 200, 200, 200, 400, 800, 200, 200, 200, 200, 200, 200, 200, 200]
        for n in range(len(notes)):
            buzz = PWM(Pin(14, Pin.OUT), freq=notes[n], duty=512)
            await asyncio.sleep_ms(tempo[n])
        
            buzz.deinit()

    async def invalid():
        pass