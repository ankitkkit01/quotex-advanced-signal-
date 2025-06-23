import websocket
import json
import threading
import time

class Quotex:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.websocket = None
        self.connected = False
        self.session_id = None

    def connect(self):
        self.websocket = websocket.WebSocketApp(
            "wss://quotexapi.site/socket.io/?EIO=3&transport=websocket",
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.thread = threading.Thread(target=self.websocket.run_forever)
        self.thread.start()
        time.sleep(2)  # Wait for connection

    def on_open(self, ws):
        self.connected = True
        print("✅ WebSocket Connected")

    def on_close(self, ws, close_status_code, close_msg):
        self.connected = False
        print("❌ WebSocket Closed")

    def on_error(self, ws, error):
        print(f"❗ WebSocket Error: {error}")

    def on_message(self, ws, message):
        if 'sid' in message:
            try:
                data = json.loads(message.split('42["",')[1].rstrip(']'))
                if 'sid' in data:
                    self.session_id = data['sid']
            except Exception:
                pass

    def login(self):
        login_payload = {
            "email": self.email,
            "password": self.password,
            "type": "personal"
        }
        data = f'42["login", {json.dumps(login_payload)}]'
        self.websocket.send(data)
        time.sleep(2)

    def check_connect(self):
        return self.connected

    def close(self):
        if self.websocket:
            self.websocket.close()

    # ❗ Add your subscribe/unsubscribe/get_candles methods here later
