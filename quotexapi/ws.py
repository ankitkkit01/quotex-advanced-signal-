import websocket

class QuotexWs:
    def __init__(self, client):
        self.client = client

    def connect(self):
        print("Connecting to Quotex WebSocket...")
