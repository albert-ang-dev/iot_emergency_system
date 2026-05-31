import bluetooth
import time

# UUIDs for the Nordic UART Service (NUS)
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)
_UART_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE | bluetooth.FLAG_WRITE_NO_RESPONSE)
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX))

class ESP32BLE:
    def __init__(self, name="ESP32_BLE"):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        
        # Register the UART service and extract the handles
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        
        self._connections = set()
        self._rx_buffer = bytearray()
        self._handler = None
        
        # Start advertising
        self._advertise(name)

    def _irq(self, event, data):
        # Handle connection
        if event == 1:  # _IRQ_CENTRAL_CONNECT
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("Device connected!")
        # Handle disconnection
        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            print("Device disconnected. Re-advertising...")
            self._advertise()
        # Handle data received
        elif event == 3:  # _IRQ_GATTS_WRITE
            conn_handle, value_handle = data
            if value_handle == self._rx_handle:
                data_received = self._ble.gatts_read(self._rx_handle)
                if self._handler:
                    self._handler(data_received)

    def send(self, data_str):
        """Converts a string to bytes and sends it to all connected devices."""
        for conn_handle in self._connections:
            try:
                self._ble.gatts_notify(conn_handle, self._tx_handle, data_str.encode('utf-8'))
            except Exception as e:
                print("Error sending data:", e)

    def on_receive(self, callback):
        """Registers a function to handle incoming strings."""
        def bytes_to_str_callback(data_bytes):
            try:
                decoded_str = data_bytes.decode('utf-8').strip()
                callback(decoded_str)
            except UnicodeError:
                print("Received non-UTF-8 data")
        self._handler = bytes_to_str_callback

    def _advertise(self, name="ESP32_BLE"):
        # Payload format: [length, type, data]
        payload = bytearray([2, 0x01, 0x06, len(name) + 1, 0x09]) + name.encode('utf-8')
        self._ble.gap_advertise(100000, adv_data=payload)
        
    def is_connected(self):
        return len(self._connections) > 0    
