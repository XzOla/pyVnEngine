import pygame
import assets
import texts

pygame.init()

#commands
screen = pygame.display.set_mode((1280, 720))
show = screen.blit
image = assets.get_image
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
music = pygame.mixer.music
# пример:
# music.play(путь до файла)
sound = pygame.mixer.Sound
# sound.play(путь до файла)
# аналогично с загрузкой аудиофайла.
font = pygame.font.Font("font.otf", 26)
font_small = pygame.font.Font("font.otf", 17)
text_manager = texts.TextManager(screen, font)

#images short name
rika = 'rika.jpg'

#music short name
memory = 'assets/music/memory.mp3'

#States
done = False
isGameDone = False
in_game = False
in_settings = False
in_menu = True
selectedButton = 0
selectedButtonInSettings = 0
selectedButtonInGameMenu = 0
music_started = False
text_window = True
is_can_show_game_menu = True
current_reading = 0




def main_menu():
    #start game
    if selectedButton == 0:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 160, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 160, 300, 60))
    #settings
    if selectedButton == 1:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 260, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 260, 300, 60))
    #quit
    if selectedButton == 2:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 360, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 360, 300, 60))

    start_text = font.render('НАЧАТЬ ИГРУ', True, (0, 0, 0))
    show(start_text, (110, 180))
    settings_text = font.render('НАСТРОЙКИ', True, (0, 0, 0))
    show(settings_text, (115, 280))
    quit_text = font.render('ВЫХОД', True, (0, 0, 0))
    show(quit_text, (140, 380))

def settings():
    #CHAR DELAY MS +-s
    if selectedButtonInSettings == 0:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 160, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 160, 300, 60))
    #MUSIC VOLUME
    if selectedButtonInSettings == 1:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 260, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 260, 300, 60))
    #SOUND VOLUME
    if selectedButtonInSettings == 2:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 360, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 360, 300, 60))
    character_delay_text = font_small.render(f"ЗАДЕРЖКА ВЫВОДА СИМВОЛОВ {texts.char_delay_ms}", True, (0, 0, 0))
    show(character_delay_text, (55, 185))
    settings_text = font.render('ГРОМКОСТЬ МУЗЫКИ', True, (0, 0, 0))
    show(settings_text, (80, 280))
    quit_text = font.render('ГРОМКОСТЬ ЗВУКА', True, (0, 0, 0))
    show(quit_text, (80, 380))

def game():
    global music_started


    if current_reading == 5:
        show(image(rika),(0, 0))
        if not music_started:
            music.load(memory)
            music.play(-1)
            music_started = True
    if current_reading == 10:
        game_quit()

def game_quit():
    global in_game
    global in_menu
    music.stop()
    in_game = False
    in_menu = True

def draw_game_menu():
    alpha_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
    pygame.draw.rect(alpha_surface, (255, 255, 255, 128), alpha_surface.get_rect())
    screen.blit(alpha_surface, (0, 0))
    menu_text = font.render('МЕНЮ ИГРЫ', True, (0, 0, 0))
    screen.blit(menu_text, (1280//2 - menu_text.get_width()//2, 100))

    if selectedButtonInGameMenu == 0:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 160, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 160, 300, 60))
    if selectedButtonInGameMenu == 1:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 260, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 260, 300, 60))
    if selectedButtonInGameMenu == 2:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 360, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 360, 300, 60))
    continue_text = font.render('ПРОДОЛЖИТЬ', True, (0, 0, 0))
    show(continue_text, (110, 180))
    settings_text = font.render('НАСТРОЙКИ', True, (0, 0, 0))
    show(settings_text, (115, 280))
    quit_text = font.render('ВЫХОД', True, (0, 0, 0))
    show(quit_text, (140, 380))

def quit_game(self):
    self.isGameDone = True

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        #Обработка нажатий кнопок в меню
        if event.type == pygame.KEYDOWN and in_game==False and in_settings==False and in_menu==True:
            #Переключение между кнопками
            if event.key == pygame.K_DOWN:
                selectedButton = (selectedButton + 1) % 3
            if event.key == pygame.K_UP:
                selectedButton = (selectedButton - 1) % 3
            #Нажатие Enter
            if event.key == pygame.K_RETURN:
                if selectedButton == 0:
                    in_menu = not in_menu
                    in_game = not in_game
                if selectedButton == 1:
                    in_menu = not in_menu
                    in_settings = not in_settings
                if selectedButton == 2:
                    done = True
        #Обработка нажатий в игре
        if event.type == pygame.KEYDOWN and in_game and not in_settings and not in_menu:
            if event.key == pygame.K_RETURN:
                if text_window:
                    if text_manager.on_click():
                        current_reading += 1
                        print(f"Текущее значение: {current_reading}")
            #Скрыть текстовое окно
            if event.key == pygame.K_SPACE and is_can_show_game_menu:
                if not text_window:
                    text_window = True
                else:
                    text_window = False

            #Показать меню в игре
            if event.key == pygame.K_ESCAPE:
                #Показываем меню в игре
                if is_can_show_game_menu:
                    is_can_show_game_menu=False
                    text_window = False
                #Скрываем меню в игре
                else:
                    is_can_show_game_menu = True
                    text_window = True

            if not is_can_show_game_menu:
                if event.key == pygame.K_DOWN:
                    selectedButtonInGameMenu = (selectedButtonInGameMenu + 1) % 3
                if event.key == pygame.K_UP:
                    selectedButtonInGameMenu = (selectedButtonInGameMenu - 1) % 3


        if event.type == pygame.MOUSEBUTTONDOWN and in_game and not in_settings:
            if event.button == 1:
                if text_window:
                    if text_manager.on_click():
                        current_reading += 1
                        print(f"Текущее значение: {current_reading}")

        # Обработка нажатий в настройках
        if event.type == pygame.KEYDOWN and in_settings and not in_game and not in_menu:
            #Выход
            if event.key == pygame.K_ESCAPE:
                selectedButtonInSettings = 0
                selectedButton = 0
                in_menu = True
                in_settings = not in_settings
            #Переключение между кнопками
            if event.key == pygame.K_DOWN:
                selectedButtonInSettings = (selectedButtonInSettings + 1) % 3
            if event.key == pygame.K_UP:
                selectedButtonInSettings = (selectedButtonInSettings - 1) % 3

            if event.key == pygame.K_RIGHT:
                if selectedButtonInSettings == 0:
                    if texts.char_delay_ms < 1000:
                        texts.char_delay_ms += 10

            if event.key == pygame.K_LEFT:
                if selectedButtonInSettings == 0:
                    if texts.char_delay_ms > 9:
                        texts.char_delay_ms -= 10

    screen.fill((0, 0, 0))
    if not isGameDone:
        if in_game:
            game()
            if text_window:
                text_manager.draw(current_reading)
            if not is_can_show_game_menu and not in_menu and not in_settings:
                draw_game_menu()
        elif in_settings:
            settings()
        elif in_menu:
            main_menu()
        else:
            main_menu()
    else:
        done = True
    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()