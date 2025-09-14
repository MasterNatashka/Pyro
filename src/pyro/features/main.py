import cv2
import numpy as np

from archive import VideoArchive
from detect import detect

# Захват видеопотока по url-адресу
cap = cv2.VideoCapture(0)
# Параметры видеопотока: частота кадров, ширина, высота
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# Создание видеоархива
archive = VideoArchive(fps, width, height)

while True:
    ok, frame = cap.read()
    if not ok:
        print("Не удалось получить кадр или видео закончилось")
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 1 запись в архив
    archive.write(frame) # запись кадра в архив
    # 2 Детекция классов
    frame_with_detection = detect(frame)


    # показать окно с видеокадрами=видеопотоком (вывод видеокадов на экран)
    cv2.imshow("W", np.hstack((frame, frame_with_detection)))

    # 3 передача видео клиенту


cap.release() # освобождение ресурсов
cv2.destroyAllWindows() # закрыть все окна