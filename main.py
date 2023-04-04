import pygame
import time
import math
import player
import world
import interface
import enemies

pygame.init()
pygame.mixer.init()

FPS = 60
WIN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
HEIGHT = WIN.get_height()
WIDTH= WIN.get_width()

pygame.display.set_caption("Sun City Sword and Shield")

def display_fps(clock):
    # display fps at the top of the screen
    font = pygame.font.Font('fonts/dogicapixel.ttf', int(WIDTH/70))
    text = font.render("FPS: " + str(int(clock.get_fps())), 1, (255,255,255))
    WIN.blit(text, (10,10))

def display_hitbox(hitbox):
    for hb in hitbox:
        pygame.draw.rect(WIN, (255,0,0), hb, 2)
    pygame.draw.rect(WIN, (0,0,255), hitbox[1], 2)

def render_player(player1, ground, spikes, keys_pressed, release_up_key, release_space_key, frame, game_world, margin_horizontal, margin_vertical, hit_timer, hit_timer_max):
    player_hitbox, player_image = player1.render_player(ground, spikes, keys_pressed, release_up_key, release_space_key, frame)
    # check if player get hit and if he is, start counting the time
    if player1.get_get_hit():
        hit_timer = time.time()
        player1.set_get_hit(False)
    
    # if the time is smaller than 1 second, gigle the player
    if time.time() - hit_timer < hit_timer_max:
        player1.set_invencible(True)
        if frame % 4 == 0:
            #make player opacity change
            player_image.set_alpha(50)
        elif(frame % 4 == 2):
            # game_world.translate(-10, 0)
            # player_hitbox.x -= 10
            player_image.set_alpha(255)
    else:
        player_image.set_alpha(255)
        player1.set_invencible(False)
    #make camera follow player
    follow_x_n, follow_x_p, follow_y_n, follow_y_p = game_world.follow()
    if(player_hitbox.x < margin_horizontal and follow_x_n):
        game_world.translate(margin_horizontal - player_hitbox.x, 0)
        player_hitbox.x = margin_horizontal
    elif(player_hitbox.x > WIDTH - margin_horizontal and follow_x_p):
        game_world.translate(WIDTH - margin_horizontal - player_hitbox.x, 0)
        player_hitbox.x = WIDTH - margin_horizontal
    if(player_hitbox.y < margin_vertical and follow_y_n):
        game_world.translate(0, margin_vertical - player_hitbox.y)
        player_hitbox.y = margin_vertical
    elif(player_hitbox.y > HEIGHT - margin_vertical and follow_y_p):
        game_world.translate(0, HEIGHT - margin_vertical - player_hitbox.y)
        player_hitbox.y = HEIGHT - margin_vertical

    game_world.check_room(player1)

    WIN.blit(player_image, player_hitbox)

    return player_hitbox, hit_timer

def main():

    game_state = "init"

    game_room = "init"

    disp_hitbox = False

    # margin of camera to player
    margin_vertical = int(HEIGHT/4)
    margin_horizontal = int(WIDTH/4)

    #init the player
    player_scale = int(WIDTH/15)
    player1 = player.Player(x = margin_horizontal, y= WIDTH/2, scale = player_scale)
    release_up_key = False
    release_down_key = False
    release_space_key = False
    frame = 0
    hit_timer = 0
    hit_timer_max = 1


    #make the level
    blocks_scale = int(WIDTH/30)
    game_world = world.Level(fase = 1, blocks_scale=blocks_scale, WHIDTH=WIDTH, HEIGHT=HEIGHT)
    game_world.set_level(player1)

    # init the interfaces
    initial_menu = interface.InitialScreen(WIDTH, HEIGHT)

    menu = interface.Menu(WIDTH, HEIGHT)

    #init the sounds
    general_volume = 1
    playing_music = False
    playing_SEF = False
    epic = pygame.mixer.Sound('musics/epic.mp3')
    entrance = pygame.mixer.Sound('musics/entrance.aiff')
    timer_music = 0
    timer_SEF = 0
    current_music = epic

    
    #RUN THE GAME
    clock = pygame.time.Clock()
    run = True
    while run:
        frame += 1
        clock.tick(FPS)

        if game_state == "run":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        player1.set_sword(not player1.get_sword())
                    if event.key == pygame.K_d:
                        player1.set_shield(not player1.get_shield())
                    if event.key == pygame.K_h:
                        disp_hitbox = not disp_hitbox
                    if event.key == pygame.K_j:
                        player1.set_can_double_jump(not player1.get_can_double_jump())
                    if event.key == pygame.K_k:
                        player1.set_can_dash(not player1.get_can_dash())
                    #reset player position to test
                    if event.key == pygame.K_r:
                        game_world.go_to_room(0,0,player1)
                    if event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                    if event.key == pygame.K_i:
                        player1.set_get_hit(True)
                
            keys_pressed = pygame.key.get_pressed()

            game_world.render_level(WIN)
            ground, spikes = game_world.get_hitboxes()
            hitboxes = game_world.hitboxes()

            player_hitbox, hit_timer = render_player(player1, ground, spikes, keys_pressed, release_up_key, release_space_key, frame, game_world, margin_horizontal, margin_vertical, hit_timer, hit_timer_max)
            
            # display hitbox
            if(disp_hitbox):
                hitbox = []
                hitbox.append(player_hitbox)
                hitbox.extend(hitboxes)
                display_hitbox(hitbox)

        elif game_state == "init":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if(initial_menu.get_actual_button() == 'Exit'):
                            run = False
                        else:
                            game_state = "run"
                            game_room = "entrance"
                            pygame.mixer.Sound.fadeout(current_music, 1000)
                            entrance.set_volume(0.5*general_volume)
                            pygame.mixer.Sound.play(entrance)
                            playing_music = False
            
            keys_pressed = pygame.key.get_pressed()

            initial_menu.render(WIN, keys_pressed, release_up_key, release_down_key)

        elif game_state == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "run"
                    if event.key == pygame.K_RETURN:
                        choice = menu.get_choice()
                        print(choice)
                        if choice == 'Resume':
                            game_state = "run"
                        elif choice == 'Exit':
                            run = False
                if(menu.exit(event)):
                    run = False
            #create menu
            keys_pressed = pygame.key.get_pressed()
            menu.render(WIN, keys_pressed, general_volume, release_up_key, release_down_key)

            if game_state == "run":
                menu.set_display(False)

        # make the mixer play the music
        if(game_room == 'init'):
            
            if not playing_music:
                epic.set_volume(general_volume)
                pygame.mixer.Sound.play(epic)
                current_music = epic
                timer_music = time.time()
                playing_music = True
            
            if time.time() - timer_music > current_music.get_length():
                playing_music = False

        keys_pressed = pygame.key.get_pressed()
        
        if not keys_pressed[pygame.K_UP]:
            release_up_key = True
        else:
            release_up_key = False

        if not keys_pressed[pygame.K_SPACE]:
            release_space_key = True
        else:
            release_space_key = False

        if not keys_pressed[pygame.K_DOWN]:
            release_down_key = True
        else:
            release_down_key = False

        display_fps(clock)
        
        pygame.display.update()        

    pygame.quit()

if __name__ == "__main__":
    main()      