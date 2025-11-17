import pygame
import os


_image_library = {}





def get_image(filename):
    global _image_library

    # Автоматически добавляем путь к папке со спрайтами
    path = os.path.join('assets', 'sprites', filename)

    image = _image_library.get(path)
    if image is None:
        # Проверяем существование файла
        if not os.path.isfile(path):
            print(f"Файл не найден: {path}")
            # Создаем пустую поверхность как заглушку
            image = pygame.Surface((100, 100))
            image.fill((255, 0, 0))  # Красный квадрат для отладки
        else:
            image = pygame.image.load(path)
            _image_library[path] = image
    return image