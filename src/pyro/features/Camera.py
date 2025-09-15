import cv2
import numpy as np
from ultralytics import YOLO

from .archive import VideoArchive


# Загрузка модели YOLOv8
model = YOLO("src/pyro/features/weights/yolov8n.pt")

# Список цветов для различных классов
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
    (255, 0, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0), (128, 128, 0),
    (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128), (72, 61, 139),
    (47, 79, 79), (47, 79, 47), (0, 206, 209), (148, 0, 211), (255, 20, 147)
]

class Camera:
    def __init__(self, source):
        self._cap = cv2.VideoCapture(source)
        self._frame = None
        self._is_streaming = False
        self._is_detecting = False
        self._start()

    def __del__(self):
        self._cap.release()

    def stream(self):
        self._is_streaming = True
        while self._is_streaming:
            ok, buf = cv2.imencode(".jpg", self._frame)
            if ok:
                yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n")

    def _start(self):
        fps = int(self._cap.get(cv2.CAP_PROP_FPS))
        width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Создание видеоархива
        self._archive = VideoArchive(fps, width, height)
        while True:
            ok, frame = self._cap.read()
            if not ok:
                # TODO Попытка переподключения
                print("Не удалось получить кадр или видео закончилось")
                break
            # Запись в архив
            self._archive.write(frame) # запись кадра в архив
            # Детекция классов
            if self._is_detecting:
                frame = self._detect(frame)
            # Запись активного кадра
            if self._is_streaming:
                self._frame = frame

    def _detect(frame):
        frame_copy = frame.copy()
        # Обработка кадра с помощью модели YOLO
        results = model(frame_copy)[0]
        classes_names = results.names
        classes = results.boxes.cls.cpu().numpy()
        boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)
        for class_id, box, conf in zip(classes, boxes, results.boxes.conf):
            if conf > 0.5:
                class_name = classes_names[int(class_id)]
                color = colors[int(class_id) % len(colors)]
                x1, y1, x2, y2 = box
                cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame_copy, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return frame_copy
