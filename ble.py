import ubluetooth

class BLE():
    def __init__(self, name):        
        self.name = name
        self.msg = ""
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.is_connected = False
        self.ble.irq(self.ble_irq)
        self.register()
        
        self.advertise()


    def ble_irq(self, event, data):
        if event == 1:
            self.is_connected = True

        elif event == 2:
            self.advertise()
            self.is_connected = False

        elif event == 3:
            buffer = self.ble.gatts_read(self.rx)
            self.msg = buffer.decode('UTF-8').strip()
            
    def register(self):
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def advertise(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)