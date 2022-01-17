import uasyncio as asyncio
from machine import Pin, PWM
import uasyncio as asyncio
from time import sleep_ms

from ble import BLE

ble = BLE("rota")

servo_pin = Pin(4, Pin.OUT)
servo = PWM(servo_pin)
servo.freq(50)
servo.duty(0)

motorA = Pin(12, Pin.OUT)
motorB = Pin(13, Pin.OUT)

speed_pin = Pin(15, Pin.OUT)
speed = PWM(speed_pin)
speed.freq(100)
speed.duty(0)

async def walk():
    while speed.duty() > 0:
        speed.duty(speed.duty() - 32)
        await asyncio.sleep_ms(10)

    motorB.value(0)
    motorA.value(1)
    
    while speed.duty() < 512:
        speed.duty(speed.duty() + 32)
        await asyncio.sleep_ms(10)

async def turn_right():
    if (servo.duty() >= 105):
        return
    
    servo.duty(servo.duty() + 28)

async def reverse():
    while speed.duty() > 0:
        speed.duty(speed.duty() - 32)
        await asyncio.sleep_ms(10)

    motorA.value(0)
    motorB.value(1)
    
    while speed.duty() < 512:
        speed.duty(speed.duty() + 32)
        await asyncio.sleep_ms(10)

async def turn_left():
    if (servo.duty() <= 50):
        return
    
    servo.duty(servo.duty() - 28)

async def stop():
    while speed.duty() > 0:
        speed.duty(speed.duty() - 32)
        await asyncio.sleep_ms(10)
        
    motorA.value(0)
    motorB.value(0)

async def reset():
    servo.duty(77)
    while speed.duty() > 0:
        speed.duty(speed.duty() - 32)
        await asyncio.sleep_ms(10)
        
    motorA.value(0)
    motorB.value(0)

async def invalid():
    return

async def main():
    functions = {
        "a": walk,
        "b": turn_right,
        "c": reverse,
        "d": turn_left,
        "e": reset,
        "g": stop
    }

    while True:
        try:
            command = functions.get(ble.msg.lower(), invalid)
            await command()

            print(ble.msg)
            ble.msg = ""
        except Exception as e:
            print(e)

        await asyncio.sleep_ms(100)

asyncio.run(main())