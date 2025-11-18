import pygame
import assets
import texts

# images short name
rika = 'rika.jpg'

# music short name
memory = 'assets/music/memory.mp3'

class Main:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"[Warning] pygame.mixer.init() failed: {e}")
        self.screen = pygame.display.set_mode((1280, 720))
        self.show = self.screen.blit
        self.image = assets.get_image
        # Работает как:
        # show(image('название файла в assets/sprites/' или название переменной с названием файла), ('координата x, координата y'))
        #
        # примеры:
        # show(image('rika.jpg'),(1000, 500)) # способ 1
        #
        # rika = 'rika.jpg' # способ 2. Поместите переменную в начало.
        # show(image(rika),(1000, 500)) # способ 2
        #
        # изображения должны быть в соответствии с разрешением экрана иначе изображения будут съезжать.
        # То есть: если разрешение экрана = 1280х720 то изображение тоже должно быть 1280х720
        # Иначе придётся определять по левому верхнему углу где должно находиться изображение
        self.music = pygame.mixer.music
        # пример:
        # music.play(путь до файла)
        self.sound = pygame.mixer.Sound
        # sound.play(путь до файла)
        # аналогично с загрузкой аудиофайла.
        self.font = pygame.font.Font("font.otf", 26)
        self.font_small = pygame.font.Font("font.otf", 17)
        self.text_manager = texts.TextManager(self.screen, self.font)

        #States
        self.done = False
        self.isGameDone = False
        self.in_game = False
        self.in_settings = False
        self.in_menu = True
        self.selectedButton = 0
        self.selectedButtonInSettings = 0
        self.selectedButtonInGameMenu = 0
        self.music_started = False
        self.text_window = True
        self.is_can_show_game_menu = True
        self.current_reading = 0
        self.clock = pygame.time.Clock()



    def main_menu(self):
        #start game
        if self.selectedButton == 0:
            pygame.draw.rect(self.screen, (255, 165, 255), pygame.Rect(40, 160, 300, 60))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(40, 160, 300, 60))
        #settings
        if self.selectedButton == 1:
            pygame.draw.rect(self.screen, (255, 165, 255), pygame.Rect(40, 260, 300, 60))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(40, 260, 300, 60))
        #quit
        if self.selectedButton == 2:
            pygame.draw.rect(self.screen, (255, 165, 255), pygame.Rect(40, 360, 300, 60))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(40, 360, 300, 60))

        start_text = self.font.render('НАЧАТЬ ИГРУ', True, (0, 0, 0))
        self.show(start_text, (110, 180))
        settings_text = self.font.render('НАСТРОЙКИ', True, (0, 0, 0))
        self.show(settings_text, (115, 280))
        quit_text = self.font.render('ВЫХОД', True, (0, 0, 0))
        self.show(quit_text, (140, 380))

    def settings(self):
        #CHAR DELAY MS +-s
        if self.selectedButtonInSettings == 0:
            pygame.draw.rect(self.screen, (255, 165, 255), pygame.Rect(40, 160, 300, 60))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(40, 160, 300, 60))
        #MUSIC VOLUME
        if self.selectedButtonInSettings == 1:
            pygame.draw.rect(self.screen, (255, 165, 255), pygame.Rect(40, 260, 300, 60))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(40, 260, 300, 60))
        #SOUND VOLUME
        if self.selectedButtonInSettings == 2:
            pygame.draw.rect(self.screen, (255, 165, 255), pygame.Rect(40, 360, 300, 60))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(40, 360, 300, 60))
        character_delay_text = self.font_small.render(f"ЗАДЕРЖКА ВЫВОДА СИМВОЛОВ {texts.char_delay_ms}", True, (0, 0, 0))
        self.show(character_delay_text, (55, 185))
        settings_text = self.font.render('ГРОМКОСТЬ МУЗЫКИ', True, (0, 0, 0))
        self.show(settings_text, (80, 280))
        quit_text = self.font.render('ГРОМКОСТЬ ЗВУКА', True, (0, 0, 0))
        self.show(quit_text, (80, 380))

    def game(self):
        if self.current_reading == 5:
            self.show(self.image(rika),(0, 0))
            if not self.music_started:
                self.music.load(memory)
                self.music.play(-1)
                self.music_started = True
        if self.current_reading == 10:
            self.game_quit()

    def game_quit(self):
        self.music.stop()
        self.in_game = False
        self.in_menu = True

    def draw_game_menu(self):
        alpha_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        pygame.draw.rect(alpha_surface, (255, 255, 255, 128), alpha_surface.get_rect())
        self.screen.blit(alpha_surface, (0, 0))
        menu_text = self.font.render('МЕНЮ ИГРЫ', True, (0, 0, 0))
        self.screen.blit(menu_text, (1280//2 - menu_text.get_width()//2, 100))

        if self.selectedButtonInGameMenu == 0:
            pygame.draw.rect(self.screen, (255, 165, 255), pygame.Rect(40, 160, 300, 60))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(40, 160, 300, 60))
        if self.selectedButtonInGameMenu == 1:
            pygame.draw.rect(self.screen, (255, 165, 255), pygame.Rect(40, 260, 300, 60))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(40, 260, 300, 60))
        if self.selectedButtonInGameMenu == 2:
            pygame.draw.rect(self.screen, (255, 165, 255), pygame.Rect(40, 360, 300, 60))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(40, 360, 300, 60))
        continue_text = self.font.render('ПРОДОЛЖИТЬ', True, (0, 0, 0))
        self.show(continue_text, (110, 180))
        settings_text = self.font.render('НАСТРОЙКИ', True, (0, 0, 0))
        self.show(settings_text, (115, 280))
        quit_text = self.font.render('ВЫХОД', True, (0, 0, 0))
        self.show(quit_text, (140, 380))

    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

                #Обработка нажатий кнопок в меню
                if event.type == pygame.KEYDOWN and self.in_game==False and self.in_settings==False and self.in_menu==True:
                    #Переключение между кнопками
                    if event.key == pygame.K_DOWN:
                        self.selectedButton = (self.selectedButton + 1) % 3
                    if event.key == pygame.K_UP:
                        self.selectedButton = (self.selectedButton - 1) % 3
                    #Нажатие Enter
                    if event.key == pygame.K_RETURN:
                        if self.selectedButton == 0:
                            self.in_menu = False
                            self.in_game = True
                        if self.selectedButton == 1:
                            self.in_menu = not self.in_menu
                            self.in_settings = not self.in_settings
                        if self.selectedButton == 2:
                            self.done = True
                #Обработка нажатий в игре
                if event.type == pygame.KEYDOWN and self.in_game and not self.in_settings and not self.in_menu:
                    if event.key == pygame.K_RETURN:
                        if self.text_window:
                            if self.text_manager.on_click():
                                self.current_reading += 1
                                print(f"Текущее значение: {self.current_reading}")
                    #Скрыть текстовое окно
                    if event.key == pygame.K_SPACE and self.is_can_show_game_menu:
                        if not self.text_window:
                            self.text_window = True
                        else:
                            self.text_window = False

                    #Показать меню в игре
                    if event.key == pygame.K_ESCAPE:
                        #Показываем меню в игре
                        if self.is_can_show_game_menu:
                            self.is_can_show_game_menu=False
                            self.text_window = False
                        #Скрываем меню в игре
                        else:
                            self.is_can_show_game_menu = True
                            self.text_window = True

                    if not self.is_can_show_game_menu:
                        if event.key == pygame.K_DOWN:
                            self.selectedButtonInGameMenu = (self.selectedButtonInGameMenu + 1) % 3
                        if event.key == pygame.K_UP:
                            self.selectedButtonInGameMenu = (self.selectedButtonInGameMenu - 1) % 3


                if event.type == pygame.MOUSEBUTTONDOWN and self.in_game and not self.in_settings:
                    if event.button == 1:
                        if self.text_window:
                            if self.text_manager.on_click():
                                self.current_reading += 1
                                print(f"Текущее значение: {self.current_reading}")

                # Обработка нажатий в настройках
                if event.type == pygame.KEYDOWN and self.in_settings and not self.in_game and not self.in_menu:
                    #Выход
                    if event.key == pygame.K_ESCAPE:
                        self.selectedButtonInSettings = 0
                        self.selectedButton = 0
                        self.in_menu = True
                        self.in_settings = not self.in_settings
                    #Переключение между кнопками
                    if event.key == pygame.K_DOWN:
                        self.selectedButtonInSettings = (self.selectedButtonInSettings + 1) % 3
                    if event.key == pygame.K_UP:
                        self.selectedButtonInSettings = (self.selectedButtonInSettings - 1) % 3

                    if event.key == pygame.K_RIGHT:
                        if self.selectedButtonInSettings == 0:
                            if texts.char_delay_ms < 1000:
                                texts.char_delay_ms += 10

                    if event.key == pygame.K_LEFT:
                        if self.selectedButtonInSettings == 0:
                            if texts.char_delay_ms > 9:
                                texts.char_delay_ms -= 10

            self.screen.fill((0, 0, 0))
            if not self.isGameDone:
                if self.in_game:
                    self.game()
                    if self.text_window:
                        self.text_manager.draw(self.current_reading)
                    if not self.is_can_show_game_menu and not self.in_menu and not self.in_settings:
                        self.draw_game_menu()
                elif self.in_settings:
                    self.settings()
                elif self.in_menu:
                    self.main_menu()
                else:
                    self.main_menu()
            else:
                self.done = True
            pygame.display.flip()
            self.clock.tick(60)

    try:
        pygame.mixer.quit()
    except Exception:
        pass
    pygame.quit()

    def main(self):
         self.run()

if __name__ == '__main__':
    app = Main()
    app.main()

