# 创建⼀个背景为蓝⾊的 Pygame 窗⼝。
import pygame

pygame.init()
width = 800
height = 600

window = pygame.display.set_mode((width, height))

bg_color = (0, 0, 255)
window.fill(bg_color)

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
