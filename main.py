# 10) Сделайте так, чтобы при изменении значения переключателя адрес найденного объекта изменялся автоматически.

import os
import sys

import pygame
import requests

import assistance

map_request = "http://static-maps.yandex.ru/1.x/"

lon = 37.565384
lat = 55.725969
delta = 0.0009
l_arr, l_arr_ind = ['map', 'sat', 'sat,skl'], 0
params = {
    "ll": ",".join([str(lon), str(lat)]),
    "spn": ",".join([str(delta), str(delta)]),
    "l": l_arr[l_arr_ind]
}

response = requests.get(map_request, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "data\\map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()

mode_btn_rect = pygame.Rect(545, 5, 50, 50)
search_btn_rect = pygame.Rect(0, 450, 150, 150)
clear_btn_rect = pygame.Rect(150, 450, 150, 150)
switch_btn_rect = pygame.Rect(545, 65, 50, 50)


screen = pygame.display.set_mode((600, 600))

mode_btn_image = assistance.load_image('mode.png', -1)
search_btn_image = assistance.load_image('search.png')
clear_btn_image = assistance.load_image('clear.png')
switch_btn_on_image = assistance.load_image('switchON.png', -1)
switch_btn_off_image = assistance.load_image('switchOFF.png', -1)

button_img = switch_btn_off_image

screen.blit(pygame.image.load(map_file), (0, 0))
screen.blit(switch_btn_off_image, switch_btn_rect)

font = pygame.font.Font(None, 17)
#text_surface = font.render('ADDRESS', True, (255, 0, 0))
#screen.blit(text_surface, (300, 450))

pygame.display.flip()

button_state = False

def toggle_button():
    global button_state
    button_state = not button_state


def update_button():
    global button_img
    if button_state:
        button_img = switch_btn_on_image
    else:
        button_img = switch_btn_off_image
    screen.blit(button_img, (545, 65))


while True:
    flag = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove(map_file)
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if mode_btn_rect.collidepoint(event.pos):
                print(
                    f'VIEW|{l_arr[l_arr_ind]} -> {l_arr[(l_arr_ind + 1) % 3]}|'
                )
                l_arr_ind = (l_arr_ind + 1) % 3
                flag = True
            elif search_btn_rect.collidepoint(event.pos):
                toponym_to_find = input('TOPONYM: ')
                #toponym_to_find = "Москва, Лобачевского, д. 92"
                lon, lat, fAdress, postal_code = assistance.searchAdress(toponym_to_find, delta)
                if button_state:
                    text_surface = font.render(fAdress + ' ' + str(postal_code), True, (255, 0, 0))
                    screen.blit(text_surface, (300, 450))
                else:
                    text_surface = font.render(fAdress, True, (255, 0, 0))
                    screen.blit(text_surface, (300, 450))
                lon, lat = float(lon), float(lat)
                toponym_lon, toponym_lat = lon, lat
                point_flag = True
                flag = True
            elif clear_btn_rect.collidepoint(event.pos):
                print('cleared')
                try:
                    text_surface.fill((0, 0, 0))
                    screen.blit(text_surface, (300, 450))
                except:
                    pass
                point_flag = False
                flag = True
            elif switch_btn_rect.collidepoint(event.pos):
                print('TOGGLED')
                toggle_button()
                update_button()
                try:
                    if not point_flag:
                        text_surface.fill((0, 0, 0))
                        screen.blit(text_surface, (300, 450))
                    else:
                        text_surface.fill((0, 0, 0))
                        screen.blit(text_surface, (300, 450))
                        if button_state:
                            text_surface = font.render(fAdress + ' ' + str(postal_code), True, (255, 0, 0))
                            screen.blit(text_surface, (300, 450))
                        else:
                            text_surface = font.render(fAdress, True, (255, 0, 0))
                            screen.blit(text_surface, (300, 450))
                except:
                    pass


        if event.type == pygame.KEYDOWN or flag:
            if flag:
                pass
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                os.remove(map_file)
                sys.exit()
            elif event.key == pygame.K_q:
                print(f'UP|{delta} -> {delta / 2}|')
                delta /= 2
            elif event.key == pygame.K_e:
                print(f'DOWN|{delta} -> {delta * 2}|')
                delta *= 2
            elif event.key == pygame.K_LEFT:
                print(f'LEFT|{lon} -> {lon - delta}|')
                lon -= delta
            elif event.key == pygame.K_RIGHT:
                print(f'RIGHT|{lon} -> {lon + delta}|')
                lon += delta
            elif event.key == pygame.K_UP:
                print(f'TW|{lat} -> {lat + delta}|')
                lat += delta
            elif event.key == pygame.K_DOWN:
                print(f'BW|{lat} -> {lat - delta}|')
                lat -= delta
            elif event.key == pygame.K_w:
                print(
                    f'VIEW|{l_arr[l_arr_ind]} -> {l_arr[(l_arr_ind + 1) % 3]}|'
                )
                l_arr_ind = (l_arr_ind + 1) % 3

            if delta < 0.0005:
                delta = 0.0005
            if delta > 100:
                delta = 100

            if lon < -179:
                lon = -179
            elif lon > 179:
                lon = 179

            if lat < -89:
                lat = -89
            elif lat > 89:
                lat = 89
            print('DELTA:', delta)
            params["ll"] = ",".join([str(lon), str(lat)])
            params["spn"] = ",".join([str(delta), str(delta)])
            params["l"] = l_arr[l_arr_ind]
            try:
                if point_flag:
                    params["pt"] = ",".join(
                        [str(toponym_lon),
                         str(toponym_lat), 'flag'])
                else:
                    del params["pt"]
            except:
                pass
            response = requests.get(map_request, params=params)

            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(",
                      response.reason, ")")
                sys.exit(1)

            with open(map_file, "wb") as file:
                file.write(response.content)

            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()

    screen.blit(mode_btn_image, mode_btn_rect)
    screen.blit(search_btn_image, search_btn_rect)
    screen.blit(button_img, switch_btn_rect)
    screen.blit(clear_btn_image, clear_btn_rect)
    pygame.display.update()
