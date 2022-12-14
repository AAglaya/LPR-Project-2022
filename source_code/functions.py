from source_code.draw_functions import *


def character_move(name, keys, map):                                                                                    # Движение персонажа
    if keys[pygame.K_w]:
        name.move_up(map)
    if keys[pygame.K_s]:
        name.move_down(map)
    if keys[pygame.K_a]:
        name.move_left(map)
    if keys[pygame.K_d]:
        name.move_right(map)


def heart_move(heart, keys):                                                                                            # Движение сердца
    if keys[pygame.K_w]:
        heart.move_up()
    if keys[pygame.K_s]:
        heart.move_down()
    if keys[pygame.K_a]:
        heart.move_left()
    if keys[pygame.K_d]:
        heart.move_right()


def finish_button(i):                                                                                                   # Если нажата кнопка выход, закончить игру
    finished = False
    if i.type == pygame.MOUSEBUTTONDOWN:
        if 5 <= i.pos[0] <= 205 and 0 <= i.pos[1] <= 70:
            finished = True
    return finished


def roaming(name, character_position, map, border):                                                                     # Перемещение персонажей между локациями
    if 480 <= character_position[0] <= 720 and character_position[1] <= 240 and name.get_location() == 0:
        name.change_location(1)
        map.change_location(1, border)
        name.go_to_the_door(60, 400)
    elif character_position[0] <= 30 and 300 <= character_position[1] <= 520 and name.get_location() == 1:
        name.change_location(0)
        map.change_location(0, border)
        name.go_to_the_door(720, 300)
    elif 230 <= character_position[0] <= 320 and character_position[1] <= 320 and name.get_location() == 1:
        name.change_location(2)
        map.change_location(2, border)
        name.go_to_the_door(900, 700)
    elif 610 <= character_position[0] <= 712 and character_position[1] <= 320 and name.get_location() == 1:
        name.change_location(3)
        map.change_location(3, border)
        name.go_to_the_door(900, 700)
    elif 840 <= character_position[0] <= 960 and 720 <= character_position[1] and name.get_location() == 2:
        name.change_location(1)
        map.change_location(1, border)
        name.go_to_the_door(280, 340)
    elif 840 <= character_position[0] <= 960 and 720 <= character_position[1] and name.get_location() == 3:
        name.change_location(1)
        map.change_location(1, border)
        name.go_to_the_door(650, 340)


def communication(screen, name, npc, event, peaceful, exit_game, font_style):                                           # Взаимодействие персонажа с npc
    for i in range(1, 4):
        if name.get_location() == i and name.small_dist_to_npc(npc[i-1]) and npc[i-1].is_alive():
            name.set_act_mode(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 680 <= event.pos[0] <= 920 and 680 <= event.pos[1] <= 760 and not npc[i-1].is_peaceful():
                    name.set_fight_mode(True)
                elif 680 <= event.pos[0] <= 920 and 680 <= event.pos[1] <= 760 and npc[i-1].is_peaceful():
                    screen.blit(peaceful, [140, 400])
                    screen.blit(exit_game, [5, 10])                                                                     # Вывести кнопку выхода из игры
                    pygame.display.update()                                                                             # Обновить экран
                    pygame.time.wait(2000)                                                                              # Подождать (пока игрок прочитает сообщение)
                    name.set_act_mode(False)                                                                            # Выключить режим взаимодействия
                    name.set_position(850, 450)
                elif 240 <= event.pos[0] <= 480 and 680 <= event.pos[1] <= 760 and not name.get_fight_mode():
                    talk_to_npc(screen, name, npc[i-1], exit_game, font_style)
