# 1. Создайте оконное приложение, отображающее карту по координатам и в масштабе, который задаётся программно.

import os
import sys

import pygame
import requests

map_request = "http://static-maps.yandex.ru/1.x/"

lon = "37.565384"
lat = "55.725969"
delta = "0.0009"

params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
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
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
