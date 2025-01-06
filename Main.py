"""Fenetre qui rassemble tous les autres fonctions du 
jeu et doit être lancé pour faire marche le jeu"""

import pygame
import time

pygame.init()


width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("STARFIGHT")
from Settings import *

pygame.display.set_icon(cut_image(Useful_Item_sprites, 16, 16, 4, 12, 50, 50))
clock = pygame.time.Clock()
running = True
Text = pygame.font.SysFont("Arial", 20)
setup = False
from Client import *
from MainMenu import *

overlap = Background

(
    b_x,
    ov_x,
    scrollx,
) = (
    0,
    500,
    0.3,
)


while running:
    # Si on est dans le menu, on affiche le menu en fonction de son état.
    if Main_menu.inmenu:
        # Pour les inputbox
        for event in pygame.event.get():
            for box in Main_menu.inputboxes:
                box.insert(Main_menu, event)
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")
        if b_x >= width:
            b_x = -width
        if ov_x >= width:
            ov_x = -width
        b_x, ov_x = b_x + scrollx, ov_x + scrollx
        screen.blit(Background, (b_x, 0))
        screen.blit(overlap, (ov_x, 0))
        # A la fin du parti on revient dans la menu et on affiche les étoiles de tous les joueurs
        if Main_menu.state == 11:
            endscreen(player_information, screen)
        # Affichage du menu
        Main_menu.show_menu(screen)
        # Que si on a commencé le serveur
        if Main_menu.serverstarted:
            (
                Main_menu.Connected_list,
                Main_menu.name_list,
                Main_menu.map_chosen,
                Main_menu.Game_time,
                Main_menu.host_start,
            ) = Main_menu.network.send(
                (
                    Main_menu.inmenu,
                    Main_menu.map_chosen,
                    Main_menu.name,
                    Main_menu.Game_time,
                    Main_menu.host_start,
                )
            )
    else:
        # Import de tous les autres modules pour faire marcher le jeu
        if not setup:
            # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            (player_information, map_chosen, Main_menu.Game_time) = (
                Main_menu.network.send("")
            )
            from Debugger import *
            import Items
            import Enemies
            import Settings

            # Conteneur qui permet de insialiser le map choisi par le hôte
            Settings.Placeholder_map = map_chosen
            from player import *
            import Levels

            # Inisilise le joueur en fonction de certains informations issues du serveur
            player = Player(
                player_information[Main_menu.network.id]["position"],
                Levels.map.visible_sprites,
                Main_menu.network.id,
                player_information[Main_menu.network.id]["name"],
            )
            # Inisialise les autres joueurs en fonction de certains informations fourni par le server
            for id in player_information:
                if id != Main_menu.network.id and id in Main_menu.Connected_list:
                    otherPlayer(
                        player_information[id]["position"],
                        (Levels.map.visible_sprites, Levels.map.other_player_sprites),
                        id,
                        player_information[id]["name"],
                    )
            # Envoi des spawners qui seront utilisé pour synchroniser les informations des ennemies et des étoiles
            if player.id == 0:
                Main_menu.network.send_sol(Levels.map.Spawners)
            # Pour que le setup n'a lieu qu'une fois
            setup = True
            Timer = time.time()
        # Pendant que le jeu est en cours
        if time.time() - Timer <= Main_menu.Game_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYUP:
                    player.action = 0
                    player.frame = 0

            screen.fill("white")
            # Envoi ces propres informations pour que le serveur puisse les traiter ainsi que reçoit les informations des autres joueurs
            player_information = Main_menu.network.speedsend(
                {
                    "position": player.rect.center,
                    "action_frame": (player.action, player.frame),
                    "facing": player.facing,
                    "inusage": player.inusage,
                    "weaponask": player.weaponask,
                    "bowask": player.bowask,
                    "direction": player.direction,
                    "star_count": player.star_count,
                    "took_damage": player.took_damage,
                    "star_lost": player.star_lost,
                    "invincibilty": player.invincibilty,
                    "ingame": player.ingame,
                    "hp": player.hp,
                    "name": player.name,
                }
            )

            if not Levels.map.start_sync:
                i = 0
                for id in Main_menu.Connected_list:
                    if player_information[id]["ingame"]:
                        i += 1
                if i == len(Main_menu.Connected_list):
                    Levels.map.start_sync = True
            # Idem mais pour les ennemies, les items et les étoiles
            map_info = Main_menu.network.speedsend(
                (player.kill_list, round(Main_menu.Game_time - (time.time() - Timer)))
            )

            # Message d'erreur car dans le cas ou le serveur s'arrete de variable est None
            if not map_info:
                print("Unable to connect to server")
                break
            # Réinisialise certaines attributs
            player.kill_list = []
            player.weaponask = False
            player.bowask = False
            player.took_damage = False
            player.star_lost = False

            # Met à jour l'affichage du map en fonction du joueur
            Levels.map.level_draw(player, player_information, map_info, screen)
            debug_position(
                [
                    (player.rect.center, (0, 0)),
                ],
                screen,
            )
            screen.blit(
                Mini_square_text.render(
                    f"{round(Main_menu.Game_time - (time.time() - Timer))}",
                    False,
                    (0, 0, 0),
                ),
                (pygame.display.get_surface().get_width() - 100, 0),
            )
        else:
            # Actions appliqués à la fin du jeu
            screen = pygame.display.set_mode((500, 500))
            Main_menu.network.client.close()
            Main_menu.state = 11
            Main_menu.inmenu = True
            Main_menu.serverstarted = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
