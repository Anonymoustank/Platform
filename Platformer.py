
def main():

    import pygame as pg
    from random import randint, choice
    GREEN = (20, 255, 140)
    GREY = (210, 210 ,210)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    PURPLE = (255, 0, 255)
    BLACK = (0, 0, 0)

    pg.init()
    WIDTH = 500
    HEIGHT = 500
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Game")

    myfont = pg.font.SysFont('verdana', 25)

    running = True

    class Background(pg.sprite.Sprite):
        def __init__(self, image_file, location):
            pg.sprite.Sprite.__init__(self)  #call Sprite initializer
            self.image = pg.image.load(image_file)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location
    
    class Player(pg.sprite.Sprite):
        def __init__(self, color, width, height):
            super().__init__()
            
            self.image = pg.Surface([width, height])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
    
            # Draw the player (a rectangle)
            pg.draw.rect(self.image, color, [0, 0, width, height])
        
    
            # Fetch the rectangle object that has the dimensions of the image.
            self.rect = self.image.get_rect()
            self.rect.center = (int(width/2), int(height/2))

    high_score = 0
    score = 0

    block_group_list = []

    player = Player(GREEN, 25, 25)
    player.rect.x = 225
    player.rect.y = 250

    block_list = pg.sprite.Group()

    moving_block_list = []

    for i in range(1, 6):
        exec("enemy_%s = Player(PURPLE, 25, 5)" % i)
        exec("enemy_%s_speed = 0" % i, globals())
        if i != 1:
            exec("enemy_%s.rect.x = randint(0, 450)" % i)
        else:
            exec("enemy_%s.rect.x = 225" % i)
        exec("enemy_%s.rect.y = 600 - (%s * 100)" %(i, i))
        exec("block_list.add(enemy_%s)" % i)
        exec("block_group_list.append(enemy_%s)" % i)

    ref = Player(GREEN, 25, 5)
    ref.rect.x = 700
    ref.rect.y = 100
    block_list.add(ref)
    block_group_list.append(ref)
    enemy_6_speed = 0

    sprite_list = pg.sprite.Group()

    falling = False

    jumping = False

    sprite_list.add(player)

    clock = pg.time.Clock()

    fps = 60

    screen.fill(BLACK)

    dest_y = ref.rect.y

    BackGround = Background('space.jpg', [0,0])

    tab_exit = False #checks to see if the player exited the while loop by dying or hitting the exit button

    can_move = False #ensures that the player can't move before hitting the first platform
    
    fall_y = ref.rect.y

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                tab_exit = True
        keys = pg.key.get_pressed()

        if keys[pg.K_r]:
            main()
            
        on_ground = False

        for a, i in enumerate(block_group_list):
            print(a + 1)
            if abs(player.rect.x - i.rect.x) <= 30 and abs(player.rect.bottom - i.rect.top) <= 5 and falling == True and jumping == False:
                can_move = True
                falling = False
                fall_y = ref.rect.y
                if ref.rect.y == dest_y:
                    jumping = False
                if randint(0, 10) != 5:
                    if i in moving_block_list:
                        moving_block_list.remove(i)
                        exec("enemy_%s_speed = 0" % (a + 1), globals())
                    i.rect.y = i.rect.y - 500
                    i.rect.x = randint(0, 450)
                else:
                    i.rect.y = i.rect.y - 500
                    i.rect.x = randint(100, 350)
                    if i in moving_block_list:
                        moving_block_list.remove(i)
                    if randint(1, 2) == 1:
                        moving_block_list.append(i)
                        exec("enemy_%s_speed = -4" % (a + 1), globals())
                    else:
                        moving_block_list.append(i)
                        exec("enemy_%s_speed = 4" % (a + 1), globals())

                dest_y = ref.rect.y + 360
                if jumping == False and falling == False:
                    jumping = True
                on_ground = True
                break
            else:
                if on_ground == False:
                    falling = True

            if i.rect.y > HEIGHT and i != ref:
                if randint(5, 6) != 5:
                    if i in moving_block_list:
                        moving_block_list.remove(i)
                        exec("enemy_%s_speed = 0" % (a + 1), globals())
                    i.rect.y = i.rect.y - 500
                    i.rect.x = randint(0, 450)
                else:
                    i.rect.y = i.rect.y - 500
                    i.rect.x = randint(100, 350)
                    if i in moving_block_list:
                        moving_block_list.remove(i)
                    if randint(1, 2) == 1:
                        moving_block_list.append(i)
                        exec("enemy_%s_speed = -4" % (a + 1), globals())
                    else:
                        moving_block_list.append(i)
                        exec("enemy_%s_speed = 4" % (a + 1), globals())
        
        screen.fill(BLACK)
        screen.blit(BackGround.image, BackGround.rect)

        sprite_list.draw(screen)
        block_list.draw(screen)

        for a, i in enumerate(moving_block_list):
            if i != ref:
                if i.rect.x >= 485:
                    exec("enemy_%s_speed = -4" % (a + 1), globals())
                elif i.rect.x <= 25:
                    exec("enemy_%s_speed = 4" % (a + 1), globals())
                exec("speed = enemy_%s_speed" % (a + 1), globals())
                i.rect.x += speed
            
        screen.fill(BLACK)
        screen.blit(BackGround.image, BackGround.rect)

        sprite_list.draw(screen)
        block_list.draw(screen)

        
        if falling == True and jumping == False:
            if abs(ref.rect.y - fall_y) < 10:
                for i in block_group_list:
                    i.rect.y -= 1
                    dest_y = ref.rect.y
                score -= 1
            elif abs(ref.rect.y - fall_y) < 60:
                for i in block_group_list:
                    i.rect.y -= 2
                    dest_y = ref.rect.y
                score -= 2
            elif abs(ref.rect.y - fall_y) < 90:
                for i in block_group_list:
                    i.rect.y -= 3
                    dest_y = ref.rect.y
                score -= 3
            else:
                for i in block_group_list:
                    i.rect.y -= 4
                    dest_y = ref.rect.y
                score -= 4

        if len(block_group_list) != 0:
            if ref.rect.y != dest_y:
                fall_y = dest_y
                if abs(ref.rect.y - dest_y) >= 120:
                    for i in block_group_list:
                        i.rect.y += 4
                    score += 4
                elif abs(ref.rect.y - dest_y) >= 60:
                    for i in block_group_list:
                        i.rect.y += 3
                    score += 3
                elif abs(ref.rect.y - dest_y) >= 10:
                    for i in block_group_list:
                        i.rect.y += 2
                    score += 2
                else:
                    for i in block_group_list:
                        i.rect.y += 1
                    score += 1
            else:
                jumping = False
        else:
            if jumping == False:
                running = False
        
        if score > high_score:
            high_score = score

        if abs(score - high_score) > 500:
            running = False
            break

        screen.fill(BLACK)
        screen.blit(BackGround.image, BackGround.rect)

        sprite_list.draw(screen)
        block_list.draw(screen)

        textsurface = myfont.render(str(high_score), True, (WHITE))
        screen.blit(textsurface,(0,0))

        if can_move == True:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                player.rect.x -= 8
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                player.rect.x += 8

        if player.rect.left > WIDTH:
            player.rect.right = 0
        if player.rect.right < 0:
            player.rect.left = WIDTH

        block_list.update()
        sprite_list.update()

        screen.fill(BLACK)
        screen.blit(BackGround.image, BackGround.rect)

        sprite_list.draw(screen)
        block_list.draw(screen)

        textsurface = myfont.render(str(high_score), True, (WHITE))
        screen.blit(textsurface,(0,0))

        pg.display.update()

        clock.tick(fps)
    if tab_exit == False:
        while player.rect.y < HEIGHT:
            player.rect.y +=2
            screen.fill(BLACK)
            screen.blit(BackGround.image, BackGround.rect)
            sprite_list.draw(screen)
            block_list.draw(screen)
            pg.display.update()

        screen.fill(BLACK)
        textsurface = myfont.render("Final Score: " + str(high_score), True, (WHITE))
        screen.blit(textsurface, (150, 200))
        restart_prompt = myfont.render("Press r to restart", True, (WHITE))
        screen.blit(restart_prompt, (145, 300))
        pg.display.update()
        running = True
        while running:
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    running=False
            if keys[pg.K_r]:
                main()
    pg.quit()
main()