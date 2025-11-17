# texts.py
import pygame
#import time

# --- Конфигурация отображения ---
char_delay_ms = 20        # задержка на один символ (мс) при typewriter-эффекте
BOX_MARGIN = 40           # отступы от краёв экрана
BOX_HEIGHT = 200          # высота окна текста
LINE_SPACING = 6          # интерлиньяж между строками
SPEAKER_MARGIN = 8        # отступ для имени говорящего внутри бокса

# --- Словарь текстов ---
# Ключи — числа current_reading. Значение — либо строка, либо словарь {'speaker':..., 'text':...}
TEXTS = {
    1: {"speaker": "Рика", "text": "Привет. Это пример первой реплики.\nНажми, чтобы продолжить."},
    2: {"speaker": "Рика", "text": "Здесь можно писать длинные абзацы. Модуль автоматически переносит строки."},
    3: {"speaker": "???", "text": "Третья реплика — без сюрпризов."},
    4: {"speaker": "Рикуша", "text": "Нипаа..."},
    5: {"speaker": "Память", "text": "Музыка запущена, фон открыт. Вот текст сцены 5.\nМожно использовать несколько абзацев.\n\nНажми, чтобы перейти дальше."},
    6: {"speaker": None, "text": "Концовка короткая."},
    7: {"speaker": "Рика", "text": "Мда"},
    8: {"speaker": "Рика", "text": "Ты ебанат да"},
    9: {"speaker": "ГГ", "text": "конечно"},
}

class TextManager:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):

        self.screen = screen
        self.font = font

        self.screen_w, self.screen_h = screen.get_size()
        self.box_rect = pygame.Rect(
            BOX_MARGIN,
            self.screen_h - BOX_HEIGHT - BOX_MARGIN,
            self.screen_w - BOX_MARGIN * 2,
            BOX_HEIGHT,
        )

        # internal state for typing
        self.current_key = None
        self.current_text = ""     # полный текст (строка)
        self.displayed_chars = 0   # сколько символов уже показано
        self._last_tick = pygame.time.get_ticks()
        self.finished = True       # полностью показан ли текущий текст


    def _load_entry(self, key):
        """Загрузить текстовую запись по ключу и сбросить состояние набора."""
        entry = TEXTS.get(key)
        if entry is None:
            self.current_key = None
            self.current_text = ""
            self.displayed_chars = 0
            self.finished = True
            return

        text = entry['text'] if isinstance(entry, dict) else entry
        # объединяем и нормализуем строки (оставляем вручную переносы \n)
        self.current_text = str(text).replace('\r\n', '\n')
        self.displayed_chars = 0
        self._last_tick = pygame.time.get_ticks()
        self.finished = False
        self.current_key = key

    def _wrap_line(self, text, max_width):
        """Простой перенос слов: возвращает список строк, каждая вписывается в max_width."""
        words = text.split(' ')
        lines = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if self.font.size(test)[0] <= max_width:
                cur = test
            else:
                if cur != "":
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def _prepare_render_lines(self, shown_text):
        """Разбивает shown_text (включая \n) на визуальные строки с переносами по ширине."""
        paragraphs = shown_text.split('\n')
        out_lines = []
        inner_margin = 16
        max_text_width = self.box_rect.width - inner_margin * 2
        for p in paragraphs:
            wrapped = self._wrap_line(p, max_text_width)
            if not wrapped:
                out_lines.append("")  # пустая строка при двойном переносе
            else:
                out_lines.extend(wrapped)
        return out_lines

    def draw(self, key):
        """
        Отрисовать текст для ключа `key` (обычно current_reading).
        Если ключ изменился — загрузим новый текст и начнём typewriter-эффект.
        Вызывать каждый кадр из основного цикла.
        """
        # если ключ поменялся — загрузить новую запись
        if key != self.current_key:
            self._load_entry(key)

        if not self.current_key:
            return  # ничего не рисуем

        # прогресс typewriter-а
        now = pygame.time.get_ticks()
        elapsed = now - self._last_tick
        if not self.finished and elapsed >= char_delay_ms:
            # добавляем символы в соответствии с elapsed
            add = elapsed // char_delay_ms
            self.displayed_chars = min(len(self.current_text), self.displayed_chars + add)
            self._last_tick += add * char_delay_ms
            if self.displayed_chars >= len(self.current_text):
                self.finished = True

        # рисуем полупрозрачный бокс
        box_surf = pygame.Surface((self.box_rect.width, self.box_rect.height), pygame.SRCALPHA)
        box_surf.fill((0, 0, 0, 180))  # чёрный с альфой
        self.screen.blit(box_surf, (self.box_rect.x, self.box_rect.y))

        # имя говорящего (если есть)
        entry = TEXTS.get(self.current_key)
        speaker = None
        if isinstance(entry, dict):
            speaker = entry.get('speaker')
        if speaker:
            name_surf = self.font.render(str(speaker), True, (255, 255, 255))
            self.screen.blit(name_surf, (self.box_rect.x + SPEAKER_MARGIN, self.box_rect.y + SPEAKER_MARGIN))

        # текст, который нужно отобразить (с учётом отображаемых символов)
        shown_text = self.current_text[:self.displayed_chars]
        lines = self._prepare_render_lines(shown_text)

        # отрисовка строк
        start_y = self.box_rect.y + (SPEAKER_MARGIN + (self.font.get_linesize() if speaker else 0)) + 12
        x = self.box_rect.x + 16
        y = start_y
        for line in lines:
            surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(surf, (x, y))
            y += self.font.get_linesize() + LINE_SPACING

        # индикатор (стрелочка), если текст полностью показан — показываем подсказку
        if self.finished:
            hint = self.font.render(">>", True, (200, 200, 200))
            hint_x = self.box_rect.right - hint.get_width() - 12
            hint_y = self.box_rect.bottom - hint.get_height() - 12
            self.screen.blit(hint, (hint_x, hint_y))

    def on_click(self):
        """
        Вызывается при клике (левая кнопка) когда активен текст.
        Поведение:
          - если текст ещё печатается — мгновенно допечатать (и вернуть False)
          - если текст уже допечатан — вернуть True (означает: можно переходить к next current_reading)
        """
        if not self.current_key:
            return True  # нет текста — можно продвигаться

        if not self.finished:
            # мгновенно показать весь текст
            self.displayed_chars = len(self.current_text)
            self.finished = True
            return False
        else:
            # текст уже показан — дать добро на переход дальше
            return True
