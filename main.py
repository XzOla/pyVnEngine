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

#images short name
rika = 'rika.jpg'

#music short name
memory = 'assets/music/memory.mp3'

#States
done = False
in_game = False
in_settings = False
in_menu = True
selectedButton = 0
selectedButtonInSettings = 0
music_started = False
text_window = True
is_can_show_game_menu = True
current_reading = 0


font = pygame.font.Font("font.otf", 26)

text_manager = texts.TextManager(screen, font)

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

def settings():
    #CHAR DELAY MS +
    if selectedButtonInSettings == 0:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 160, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 160, 300, 60))
    #CHAR DELAY MS -
    if selectedButtonInSettings == 1:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 260, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 260, 300, 60))
    #idk lol...
    if selectedButtonInSettings == 2:
        pygame.draw.rect(screen, (255, 165, 255), pygame.Rect(40, 360, 300, 60))
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(40, 360, 300, 60))
    return

def game():
    global music_started

    if current_reading == 5:
        show(image(rika),(0, 0))
        if not music_started:
            music.load(memory)
            music.play(-1)
            music_started = True



while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        #Обработка нажатий кнопок в меню
        if event.type == pygame.KEYDOWN and in_game==False and in_settings==False and in_menu==True:
            #Переключение между кнопками
            if event.key == pygame.K_DOWN:
                selectedButton = (selectedButton + 1) % 3
                print(selectedButton)
            if event.key == pygame.K_UP:
                selectedButton = (selectedButton - 1) % 3
                print(selectedButton)
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
                    print(is_can_show_game_menu)
                #Скрываем меню в игре
                else:
                    is_can_show_game_menu = True
                    text_window = True
                    print(is_can_show_game_menu)


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
                print(selectedButtonInSettings)
            if event.key == pygame.K_UP:
                selectedButtonInSettings = (selectedButtonInSettings - 1) % 3
                print(selectedButtonInSettings)

            if event.key == pygame.K_RIGHT:
                if selectedButtonInSettings == 0:
                    if texts.char_delay_ms < 1000:
                        texts.char_delay_ms += 10
                        print(f"Текущее значение: {texts.char_delay_ms} МС")

            if event.key == pygame.K_LEFT:
                if selectedButtonInSettings == 0:
                    if texts.char_delay_ms > 9:
                        texts.char_delay_ms -= 10
                        print(f"Текущее значение: {texts.char_delay_ms} МС")


    screen.fill((0, 0, 0))


    if in_game:
        game()
        if text_window:
            text_manager.draw(current_reading)



    elif in_settings:
        settings()

    elif in_menu:
        main_menu()
    else:
        main_menu()





    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()