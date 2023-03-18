# 3. Добавьте обработку клавиш вверх/вниз/вправо/влево, по нажатию на которые необходимо перемещать центр карты в соответствующую сторону на размер экрана.

import os
import sys

import pygame
import requests

map_request = "http://static-maps.yandex.ru/1.x/"

lon = 37.565384
lat = 55.725969
delta = 0.0009

params = {
    "ll": ",".join([str(lon), str(lat)]),
    "spn": ",".join([str(delta), str(delta)]),
    "l": "map"
}

response = requests.get(map_request, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))

screen.blit(pygame.image.load(map_file), (0, 0))

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove(map_file)
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                os.remove(map_file)
                sys.exit()
            elif event.key == pygame.K_q:
                print(f'UP|{delta}|{delta / 2}|')
                delta /= 2
            elif event.key == pygame.K_e:
                print(f'DOWN|{delta}|{delta * 2}|')
                delta *= 2
            elif event.key == pygame.K_LEFT:
                print(f'LEFT|{lon}|{lon - delta}|')
                lon -= delta
            elif event.key == pygame.K_RIGHT:
                print(f'RIGHT|{lon}|{lon + delta}|')
                lon += delta
            elif event.key == pygame.K_UP:
                print(f'UP|{lat}|{lat + delta}|')
                lat += delta
            elif event.key == pygame.K_DOWN:
                print(f'DOWN|{lat}|{lat - delta}|')
                lat -= delta

            if delta < 0.00001:
                delta = 0.00001
            elif delta > 100:
                delta = 100
            
            if lon < -179:
                lon = -179
            elif lon > 179:
                lon = 179
            
            if lat < -89:
                lat = -89
            elif lat > 89:
                lat = 89

            params["ll"] = ",".join([str(lon), str(lat)])
            params["spn"] = ",".join([str(delta), str(delta)])
            response = requests.get(map_request, params=params)

            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)

            with open(map_file, "wb") as file:
                file.write(response.content)

            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
