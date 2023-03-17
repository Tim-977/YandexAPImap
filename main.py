# 2. Добавить обработку клавиш PgUp и PgDown, по нажатию на которые соответственно увеличивать и уменьшать масштаб отображения карты. Необходимо отслеживать предельные значения, за которые значения переменных не должны заходить.

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

            if delta < 0.00001:
                delta = 0.00001
            elif delta > 100:
                delta = 100

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
