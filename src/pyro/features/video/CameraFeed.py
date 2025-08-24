import cv2
import os
import requests
from requests.auth import HTTPDigestAuth


class CameraFeed:
    def __init__(self, source):
        self._source = source
        self._cap = cv2.VideoCapture(self._rtsp_url())
        self._ptz_url =  f"http://{source}:8899/onvif/ptz_service"
        self._ptz_headers = {'Content-Type': 'application/soap+xml'}
        self._ptz_auth = HTTPDigestAuth(os.environ.get("RTSP_USER"), os.environ.get("RTSP_PASSWORD"))
        self._ptz_timeout = 5

    def __del__(self):
        self._cap.release()

    def stream(self):
        while True:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + self._get_frame() + b'\r\n')

    def ptz_move(self, pan=0, tilt=0):
        # TODO проверка на крайние положения
        return requests.post(
            self._ptz_url,
            headers=self._ptz_headers,
            auth=self._ptz_auth,
            timeout=self._ptz_timeout,
            data=f"""
                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
                    <soap:Body>
                        <tptz:ContinuousMove xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">
                            <tptz:ProfileToken>Profile_1</tptz:ProfileToken>
                            <tptz:Velocity>
                                <tt:PanTilt x={pan} y={tilt} xmlns:tt="http://www.onvif.org/ver10/schema"/>
                            </tptz:Velocity>
                        </tptz:ContinuousMove>
                    </soap:Body>
                </soap:Envelope>
            """
        )

    def ptz_stop(self):
        return requests.post(
            self._ptz_url,
            headers=self._ptz_headers,
            auth=self._ptz_auth,
            timeout=self._ptz_timeout,
            data=f"""
                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
                    <soap:Body>
                        <tptz:Stop xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">
                            <tptz:ProfileToken>Profile_1</tptz:ProfileToken>
                            <tptz:PanTilt>true</tptz:PanTilt>
                            <tptz:Zoom>true</tptz:Zoom>
                        </tptz:Stop>
                    </soap:Body>
                </soap:Envelope>
            """
        )

    def _rtsp_url(self):
        if self._source == os.environ.get("TEST_CAM_ADDR"):
            return os.environ.get("TEST_CAM_ADDR2")
        user = os.environ.get("RTSP_USER")
        password = os.environ.get("RTSP_PASSWORD")
        return f"rtsp://{self._source}:554/user={user}&password={password}&channel=0&stream=1?.sdp"

    def _get_frame(self):
        try:
            ok, frame = self._cap.read()
            if not ok:
                return None
            ok, buf = cv2.imencode('.jpg', frame)
            return buf.tobytes()
        except Exception as e:
            print(f"Ошибка получения кадра: {e}")
            return None

