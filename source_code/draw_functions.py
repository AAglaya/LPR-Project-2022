import pygame


def beggining_title(screen, name, start_game_text_1, start_game_text_2):                                                # Нарисовать вступление
    screen.fill((0, 0, 0))
    start_game = True
    screen.blit(start_game_text_1, [320, 350])
    screen.blit(start_game_text_2, [320, 400])
    pygame.display.update()
    pygame.time.wait(5000)
    name.set_act_mode(False)
    return start_game


def end_title(screen, name, end_game_text):
    screen.fill((0, 0, 0))                                                                                              # Нарисовать завершение игры
    screen.blit(end_game_text, [280, 350])
    pygame.display.update()
    pygame.time.wait(3000)
    finished = True
    name.set_act_mode(False)
    return finished


def interface(screen, map, width, height, heart, font_style_small, fight, talk):                                        # Рисовать интерфейс взаимодействия
    screen.fill((0, 0, 0))
    map.draw_map(screen, width, height, 'act', 0)
    hp = font_style_small.render("HP: " + str(heart.get_hp()) + " / 5", True, (255, 0, 0))
    screen.blit(hp, [540, 660])
    screen.blit(fight, [740, 710])
    screen.blit(talk, [300, 710])


def end_fight(screen, heart, font_style, name, npc_i, Exit):
    finished = False
    finish_game = False
    name.set_fight_mode(False)                                                                                          # Выйти из режима боя
    if heart.get_hp() > 0:                                                                                              # Если hp > 0
        mark = font_style.render(npc_i.get_name() + ': Your mark is ' + str(heart.get_hp() * 2) + '/10', True,
                                 (255, 255, 255))
        name.pass_exam()                                                                                                # Зачитать сданный экзамен
        if name.show_marks() == 2:                                                                                      # Если сдано 2 экзамена
            finish_game = True                                                                                          # Закончить игру
            name.set_act_mode(True)                                                                                     # Перейти к завершающему "слайду"
    else:                                                                                                               # Иначе (если hp < 0)
        mark = font_style.render(npc_i.get_name() + ': You lost. Retake in January', True,
                                 (255, 255, 255))                                                                       # Сгенерировать сообщение о пересдаче
        finished = True                                                                                                 # Закончить игру
    pygame.draw.rect(screen, (0, 0, 0),
                     (124, 404, 940, 230))                                                                              # Залить разговорное окно чёрным (убрать сердце)
    screen.blit(mark, [140, 400])                                                                                       # Вывести сообщение о результате
    screen.blit(Exit, [5, 10])                                                                                          # Отрисовать кнопку выхода из игры
    pygame.display.update()                                                                                             # Обновить экран
    pygame.time.wait(1000)                                                                                              # Подождать (пока играющий прочтёт сообщение)
    npc_i.kill()                                                                                                        # Убить npc
    heart.set_hp(5 - heart.get_hp())                                                                                    # Восстановить hp до фулла
    name.set_position(850, 400)                                                                                         # Переместить персонажа вне зону взаимодействия с npc
    name.set_act_mode(False)                                                                                            # Выйти из режима взаимодействия
    return finished, finish_game


def draw_npc_map(screen, name, npc):                                                                                    # Отрисовать npc а карте
    for i in range(2, 5):
        if name.get_location() == i and not name.get_act_mode() and npc[i-2].is_alive():
            npc_position = npc[i-2].get_position()
            npc[i-2].draw(screen, npc_position[0], npc_position[1])


def draw_npc_act_mode(screen, name, npc):                                                                               # Отрисовать npc в режиме взаимодействия
    for i in range(2, 5):
        if name.get_location() == i:
            npc[i - 2].draw(screen, 600, 300)


def talk_to_npc(screen, name, npc_i, exit_game, font_style):                                                            # Отрисовать разговор с npc
    phrase = font_style.render(npc_i.talk(), True, (255, 255, 255))
    screen.blit(phrase, [140, 400])
    screen.blit(exit_game, [5, 10])
    pygame.display.update()
    pygame.time.wait(2000)
    name.set_act_mode(False)
    if npc_i.get_name() == 'Koldunov':
        name.set_position(950, 600)
    else:
        name.set_position(850, 450)
