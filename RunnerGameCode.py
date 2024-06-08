import pygame
from random import randint
from sys import exit

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - startTime
    score_surface = test_font.render("Score : " + str(current_time) ,False,(31,33,64)) # (31,33,64) is rgb represeation of colour
    score_rect=score_surface.get_rect(center = (400,50))
    pygame.draw.rect(screen,'#c0e8ec',score_rect)
    screen.blit(score_surface,score_rect) 
    return current_time

def enemy_spawn(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5
            if enemy_rect.bottom == 300 :
                screen.blit(enemy_snail_surface,enemy_rect)
            else:
                screen.blit(enemy_fly_surface,enemy_rect)

        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]
        return enemy_list
    
    else:
        return []

def collision(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            if player_rect.colliderect(enemy_rect) :
                    return True
        return False
    else:
        return False
    

pygame.init()
width=800
height=400

screen = pygame.display.set_mode((width,height))#here i am making the screen of this width and height
pygame.display.set_caption('Runner game')# just for the caotion of the window that appears
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = True
startTime = 0
score = 0

#colour_surface = pygame.Surface((100,200)) 
#colour_surface.fill('RED') # this is for surface to fill with colour

sky = pygame.image.load('graphics/sky.png').convert() # loading the image from this path
ground = pygame.image.load('graphics/ground.png').convert() # .convert just turns the image into some file so pygame can work eaisly

score_surface = test_font.render("Musaddiq's game",False,(31,33,64)) # (31,33,64) is rgb represeation of colour
score_rect=score_surface.get_rect(center = (400,50))

enemy_snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha() # convert alpha makes it so snail image blends properly
enemy_snail_rect = enemy_snail_surface.get_rect(midbottom = (700,300))

enemy_fly_surface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha() # convert alpha makes it so snail image blends properly
enemy_fly_rect = enemy_snail_surface.get_rect(midbottom = (700,210))

enemy_list = []

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha() 
player_rect = player_surface.get_rect(midbottom = (100,300)) # makes a rectange of the player surface so we can place it more precisely

jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.5)

game_sound = pygame.mixer.Sound('audio/music.wav')
game_sound.set_volume(0.2)
game_sound.play(loops = -1)


player_gravity = 0 
score = 0

#timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer,1500)

while True: #infitely display the screen by th display update

    for event in pygame.event.get():
        if event.type==pygame.QUIT: # if quitting then this will take input and exit the code
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                if game_active:
                    if player_rect.bottom == 300:                
                        player_gravity = -20
                        jump_sound.play()
                else:
                    player_gravity = 0
                    game_active = True
                    score = 0
                    enemy_snail_rect.midbottom = (700,300)
                    startTime = int (pygame.time.get_ticks() / 1000)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    if player_rect.bottom == 300:                
                        player_gravity = -20
                        jump_sound.play()
                else:
                    player_gravity = 0
                    game_active = True
                    score = 0
                    enemy_snail_rect.midbottom = (700,300)
                    startTime = int (pygame.time.get_ticks() / 1000)
        if event.type == enemy_timer and game_active :
            if(randint(0,2)):
                enemy_list.append(enemy_snail_surface.get_rect(midbottom = (900,300)))
            else:
                enemy_list.append(enemy_fly_surface.get_rect(midbottom = (900,210)))
            
    
    screen.blit(sky,(0,0))# put one surface onto another 
    screen.blit(ground,(0,300)) 

    
    if game_active:
        score = display_score()
        #screen.blit(enemy_snail_surface,enemy_snail_rect)
        #enemy_snail_rect.left -= 5 # move snail left 
        #if enemy_snail_rect.right <= 0:
        #    enemy_snail_rect.left = width
        
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300 :
            player_rect.bottom = 300 
        screen.blit(player_surface,player_rect) 
        # player_rect.left += 1 # makes player move right 

        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_SPACE]:

        enemy_list = enemy_spawn(enemy_list)

        if collision(enemy_list):
             game_active = False
             enemy_list.clear()
        

        #mouse_pos = pygame.mouse.get_pos() # this gets our mouse position
        #if player_rect.collidepoint(mouse_pos): # here we see if the mouse position we got touches our player
        #    if pygame.mouse.get_pressed():
        #        print('Mouse colision')
    else:

        screen.blit(enemy_snail_surface,enemy_snail_rect)
        screen.blit(player_surface,player_rect) 

        gameover_surface = test_font.render("Game Over",False,(211,33,45))
        gameover_rect = gameover_surface.get_rect(center = (400,100)) 
        screen.blit(gameover_surface,gameover_rect)
        
        Final_score_surface = test_font.render("Score : " + str(score) ,False,(31,33,64)) # (31,33,64) is rgb represeation of colour
        Final_score_rect=Final_score_surface.get_rect(center = (400,50))
        pygame.draw.rect(screen,'#c0e8ec',Final_score_rect)
        screen.blit(Final_score_surface,Final_score_rect) 
        
        restart_surface = test_font.render("Press space to restart",False,'#001A0D')
        restart_rect = restart_surface.get_rect(center = (400,200)) 
        screen.blit(restart_surface,restart_rect)

    

    pygame.display.update()    
    clock.tick(60) # insuring that our game doesn't go faster than 60 fps
