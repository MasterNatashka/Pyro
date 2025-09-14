import cv2
import os
import tempfile
import threading
import time

# Адрес папки для хранения временных видеофайлов
TEMP_DIR = "C:\\Users\\Natashka\\Desktop\\zapis-video\\video"
# Адрес папки для хранения видеофайлов
VIDEO_DIR = "C:\\Users\\Natashka\\Desktop\\zapis-video\\video"
# Продолжительность видеофайла в секундах
CHUNK_LEN = 60

# Класс записи видеофайлов с одной видеокамеры в видеоархив
class VideoArchive:
    # конструктор класса с передачей параметров для записи видеофайла. 
    def __init__(self, fps, width, height):
        self.frames_per_chunk = CHUNK_LEN * fps # создаёт атрибут количества кадров в видеофайле (кадры = секунды × кадры/секунду)
        self.fps = fps # создаёт атрибут fps у объекта видеофайл 
        self.frame_width = width # создаёт атрибут frame_width у объекта видеофайл 
        self.frame_height = height # создаёт атрибут frame_height у объекта видеофайл 
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v') # создаёт атрибут fourcc у объекта видеофайл 

        self.total_frame_count = 0 # создаёт атрибут total_frame_count (количество кадров с начала записи) у объекта
        self.chunk_start_time = None # создаёт атрибут chunk_start_time (время начала записи текущего отрезка) у объекта
        self.chunk_temp_path = None # создаёт атрибут chunk_temp_path (путь к временному видеофайлу текущего отрезка) у объекта
        self.chunk_writer = None # создаёт атрибут chunk_writer (запись кадров в текущий отрезок видеофайла) у объекта

    # используем ранее созданные атрибуты: chunk_writer и проверяем его на наличие значения (не пустой)
    def __del__(self): 
        if self.chunk_writer is not None: # проверка наличия записи видеофайла
            self.chunk_writer.release()
            # Формируем путь до основного видеофайла, включая его имя
            chunk_path = os.path.join(VIDEO_DIR, f"{int(self.chunk_start_time)}.mp4")
            # Перекодируем видеофайл из временного видеофайла в основной видеофайл
            self._save_chunk(self.chunk_temp_path, chunk_path)

    # функция записи кадра в текущий файл
    def write(self, frame): 
        if self.total_frame_count % self.frames_per_chunk == 0: # если количество кадров с начала записи кратно количеству кадров в видеофайле 
            if self.chunk_writer is not None: # проверка наличия записи видеофайла
                self._finalize_write() # метод завершения записи видеофайла
            self.chunk_start_time = time.time() # фиксируем время начала записи видеофайла для имени файла
            # Создаём временный файл с параметрами: suffix, delete, dir
            temp_file = tempfile.NamedTemporaryFile(
                suffix='.mp4', 
                delete=False,
                dir=TEMP_DIR
            )
            # Записываем в атрибут chunk_temp_path путь (name) к временному файлу из атрибута temp_file.name
            self.chunk_temp_path = temp_file.name
            # Закрываем временный файл, чтобы следующая функция смогла открыть временный файл
            temp_file.close()
            # Создаём атрибут chunk_writer для записи временного видеофайла класса VideoWriter с аргументами: chunk_temp_path, fourcc, fps, (self.frame_width, self.frame_height)
            self.chunk_writer = cv2.VideoWriter(
                self.chunk_temp_path,
                self.fourcc,
                self.fps,
                (self.frame_width, self.frame_height)
            )
        # Передаём временный кадр в функцию записи
        self.chunk_writer.write(frame)
        # Увеличиваем счетчик кадров
        self.total_frame_count += 1

    # Функция класса (равно метод!) завершения записи временного видеофайла. Временный видеофайл перекодируется в основной видеофайл и сохраняется
    def _finalize_write(self):
        # Освобождаем ресурсы предыдущей записи
        self.chunk_writer.release()
        # Формируем путь до основного видеофайла, включая его имя
        chunk_path = os.path.join(VIDEO_DIR, f"{int(self.chunk_start_time)}.mp4")
        # Записываем в переменную potok_sohranenia_video экземпляр класса Thread библиотеки threading. В потоку программы будет выполнятся функция сохранения видеофайла с аргументами пути временного видеофайла и пути основного видеофайла
        potok_sohranenia_video = threading.Thread(
            target=self._save_chunk,
            args=(self.chunk_temp_path, chunk_path)
        )
        # Запускаем параллельный поток программы, вызвав метод start
        potok_sohranenia_video.start()

    # Перекодируем видеофайл из временного видеофайла в основной видеофайл
    def _save_chunk(self, chunk_temp_path, chunk_final_path):
        # Запускаем программу ffmpeg, установленную в системе для перекодирования видеофайла,  используя кодек H265 для сжатия
        os.system(f"ffmpeg -i {chunk_temp_path} -vcodec libx265 {chunk_final_path}")
        # Удаляем временный видеофайл
        os.remove(chunk_temp_path)