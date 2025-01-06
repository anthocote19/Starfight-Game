import pygame

pygame.init()
Text = pygame.font.SysFont("Arial", 20)


def debug_position(debugs, screen):
    for debug, atposition in debugs:
        screen.blit(Text.render(f"{debug}", False, (0, 0, 0)), atposition)
