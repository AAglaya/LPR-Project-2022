from source_code.objects import *                                                                                       # Подключение модулей
from source_code.constants import *
from source_code.functions import *
from source_code.draw_functions import *

finished = False                                                                                                        # Создание основных переменных для работы игры
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))
timer = 0

pygame.init()                                                                                                           # Запуск игры

font_style = pygame.font.SysFont('cambria', 50)
font_style_start = pygame.font.SysFont('cambria', 100)
font_style_small = pygame.font.SysFont('cambria', 25)

exit_game = font_style.render("Exit", True, (255, 0, 0))
fight = font_style.render("Fight", True, (255, 0, 0))                                                                   # Создание сообщений, которые будут выводиться на экран
talk = font_style.render("Talk", True, (0, 255, 0))
start_game_text_1 = font_style_small.render("Oh, my head so hurts. Why i am hear? What time is it?...",
                                            True, (255, 255, 255))
start_game_text_2 = font_style_small.render("Oh no, my exam starts in 10 minutes, i have to hurry",
                                            True, (255, 255, 255))
end_game_text = font_style_small.render("You passed all exams. Congratulations!", True, (255, 255, 255))
peaceful = font_style.render("It's not worth fighting with LM...", True, (255, 255, 255))

map = Map(0, border)                                                                                                    # Создание карты
name = MainCharacter(700, 600, 0)                                                                                       # Создание главного героя
heart = Heart('models/heart.bmp', 595, 520, 5, 5)                                                                       # Создание сердца
npc1 = NPC('Koldunov', 'models/Koldunov.bmp', 1000, 600, phrases_1)                                                     # Создание npc1 (КЛМ)
npc2 = NPC('Nikolaenko', 'models/Nikolaenko.bmp', 880, 370, phrases_2)                                                  # Создание npc2 (Николаенко)
npc3 = NPC('Zhdanovskii', 'models/Zhdanovskii.bmp', 880, 370, phrases_2)                                                # Создание npc3 (Ждановский)

write_message_about_peaceful = False                                                                                    # Создание флаговых переменных
choose_lvl = False
start_fire_1 = False
start_fire_2 = False
start_game = False
finish_game = False
time_fire = 0
level = 1

name.set_act_mode(True)                                                                                                 # Установить режим коммуникации

while not finished:                                                                                                     # Пока игра не закончилась
    if not choose_lvl:
        level, choose_lvl = choose_level(screen, font_style_start, choose_lvl)
    if finish_game:                                                                                                     # Если игра заканчивается
        finished = end_title(screen, name, end_game_text)
    if name.get_act_mode():                                                                                             # Если активирован режим взаимодействия
        if not start_game:                                                                                              # Если игра только начинается
            start_game = beggining_title(screen, name, start_game_text_1, start_game_text_2)
        interface(screen, map, width, height, heart, font_style_small, fight, talk)                                     # Отрисовать интерфейс взаимодействия
        draw_npc_act_mode(screen, name, [npc1, npc2, npc3])
    else:
        screen.fill((255, 255, 255))                                                                                    # Отрисовать карту
        phase = int(timer * 1.5) % 2
        map.draw_map(screen, width, height, 'map', phase)
        name.draw_character(screen)

    if name.get_fight_mode():                                                                                           # Если персонаж в режиме боя
        if name.get_location() == 3:                                                                                    # Если персонаж дерётся в локации 2
            heart.draw_heart(screen)                                                                                    # Отрисовать сердце
            if npc2.get_number_of_shots_type1() <= 10:                                                                  # Если npc2 ещё не сделал 10 залпов
                if not start_fire_1 or (
                        start_fire_1 and timer - time_fire >= 1 / level):                                               # Если огонь ещё не открыт или между залпами прошла секунда
                    npc2.fire_type1()                                                                                   # Дать залп типа 1
                    start_fire_1 = True                                                                                 # Записать в переменную, что открыт огонь
                    time_fire = timer                                                                                   # Записать время залпа
            elif npc2.get_number_of_shots_type1() > 10 and timer - time_fire >= 2:                                      # Если сделано больше 10 залпов и с момента последнего прошло больше 2 секунд
                finished, finish_game = end_fight(screen, heart, font_style, name, npc2, exit_game)

        if name.get_location() == 4:                                                                                    # Если бой в локации номер 3
            heart.draw_heart(screen)                                                                                    # Код ниже аналогично коду, описывающему бой в локации 2
            if npc3.get_number_of_shots_type2() <= 5:                                                                   # Изменены тайминги взаимодействия
                if not start_fire_2 or (start_fire_2 and timer - time_fire >= 4 / level):
                    npc3.fire_type2()
                    start_fire_2 = True
                    time_fire = timer
            elif npc3.get_number_of_shots_type2() > 5 and timer - time_fire >= 8:
                finished, finish_game = end_fight(screen, heart, font_style, name, npc3, exit_game)

    clock.tick(FPS)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            finished = True

        finished = finish_button(i)

        keys = pygame.key.get_pressed()
        if keys and not name.get_act_mode():
            character_move(name, keys, map)
        if keys and name.get_fight_mode():
            heart_move(heart, keys)
        else:
            communication(screen, name, [npc1, npc2, npc3], i, peaceful, exit_game, font_style)

    for bullet in bullets:                                                                                              # Отрисовать все пули (шарики)
        bullet.draw(screen)
        bullet.move()
        if bullet.hittest(heart):                                                                                       # При столкновении удалить пулю из списка
            heart.set_hp(-1)
            bullets.remove(bullet)

    for bone in bones:                                                                                                  # Отрисовать все кости аналогично
        bone.draw(screen)
        heart.draw_heart(screen)
        bone.move()
        if bone.hittest(heart):
            heart.set_hp(-1)
            bones.remove(bone)
        if bone.is_bone_dangerous():
            bones.remove(bone)

    character_position = name.get_position()
    roaming(name, character_position, map, border)

    draw_npc_map(screen, name, [npc1, npc2, npc3])
    screen.blit(exit_game, [5, 10])                                                                                     # Нарисовать кнопку выход из игры

    timer += 1 / 120                                                                                                    # Обновить таймер
    pygame.display.update()                                                                                             # Обновить экран