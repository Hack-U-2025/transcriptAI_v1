import unittest
from app import app, socketio


class TestFlaskSocketIO(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.socketio_test_client = socketio.test_client(app)

    def tearDown(self):
        self.socketio_test_client.disconnect()

    def test_start_transcription_event(self):
        # WebSocket接続確認
        connected = self.socketio_test_client.is_connected()
        self.assertTrue(connected)

        # start_transcription_unityイベント送信
        self.socketio_test_client.emit("start_transcription_unity")

        # transcription_unityイベント受信確認
        received = self.socketio_test_client.get_received()
        self.assertTrue(
            any(event["name"] == "transcription_unity" for event in received)
        )


if __name__ == "__main__":
    unittest.main()
