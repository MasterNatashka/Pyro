import cv2
import os


class CameraFeed:
    def __init__(self, source):
        self.source = source
        self.cap = cv2.VideoCapture(self.rtsp_url())

    def __del__(self):
        if hasattr(self, "cap"):
            self.cap.release()

    def rtsp_url(self):
        if self.source == os.environ.get("TEST_CAM_ADDR"):
            return os.environ.get("TEST_CAM_RTSP")
        user = os.environ.get("RTSP_USER")
        password = os.environ.get("RTSP_PASSWORD")
        return f"rtsp://{self.source}:554/user={user}&password={password}&channel=0&stream=1?.sdp"

    def ptz_url(self):
        return f"http://{self.source}:8899/onvif/ptz_service"

    def get_frame(self):
        try:
            ok, frame = self.cap.read()
            if not ok:
                return None
            ok, buf = cv2.imencode('.jpg', frame)
            return buf.tobytes()
        except Exception as e:
            print(f"Ошибка получения кадра: {e}")
            return None

    def stream(self):
        while True:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + self.get_frame() + b'\r\n')
