import pygame
import random

pygame.init()

width, height = size = 1200, 720
w_b, h_b = 100, 20
border_size = 5
FONT_SIZE = 20
R = 16 # Ball's Radius

#win = pygame.image.load('win.jpg')
player_win = None
file_img_fon = ['space1.jpg', 'space2.jpg']
img_fon = pygame.transform.scale(pygame.image.load(random.choice(file_img_fon)), (width, height))

delta = 1
MYEVENTTYPE = 30
pygame.time.set_timer(MYEVENTTYPE, 2000)





PLAY = True
running = True

motion1 = 0
motion2 = 0
speed = 20
w, h = 200, 5




ball_speed = 1


screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fon = pygame.sprite.Group()
spr_fon = pygame.sprite.Sprite()
spr_fon.image = img_fon
spr_fon.rect = spr_fon.image.get_rect()
spr_fon.add(fon)
good_blocks = pygame.sprite.Group()
balls_sprites = pygame.sprite.Group()
walls_sprites = pygame.sprite.Group()

win = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
texts = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()



def restart():
    for spr in good_blocks.sprites():
        for i in spr.borders:
            i.kill()
        spr.kill()


class Ball(pygame.sprite.Sprite):
    imgs = ['ball1.png', 'ball2.png', 'ball3.png']
    img = pygame.image.load(random.choice(imgs))
    def __init__(self, radius, x, y, group):
        super().__init__()
        self.radius = radius
        self.image = pygame.transform.scale(Ball.img, (radius * 2, radius * 2))
        self.image.set_colorkey(-1)
        #self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)

        #pygame.draw.circle(self.image, pygame.Color("red"),(radius, radius), radius)

        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.choice([-ball_speed, ball_speed])
        self.vy = random.choice([-ball_speed, ball_speed])
        self.add(group)

    def update(self):
        global player_win
        global PLAY

        if(self.rect.y <= border_size + 7 ):
            PLAY = False
            player_win = pygame.transform.scale(pygame.image.load('win2.gif'), (int(width / 1.5), int(height / 2.5)))

        if(self.rect.y  + 2 * R >= height - border_size - 7):
            PLAY = False
            player_win = pygame.transform.scale(pygame.image.load('win1.gif'), (int(width / 1.5), int(height / 2.5)))

        self.vx = (self.vx // (abs(self.vx))) * ball_speed
        self.vy = (self.vy // (abs(self.vy))) * ball_speed
        self.rect = self.rect.move(self.vx, self.vy)

        res = pygame.sprite.spritecollideany(self, good_blocks)
        if res != None:
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
                self.rect.y += self.vy * 1.2

            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
                self.rect.x += self.vx * 1.2

            res.cnt -= 1
            res.change_text()
            res.update()

        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
            self.rect.y += self.vy * 1.2

        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
            self.rect.x += self.vx * 1.2


        if(self.rect.y < border_size + 5 ):
            PLAY = False
            player_win = pygame.transform.scale(pygame.image.load('win2.gif'), (int(width / 1.5), int(height / 2.5)))

        if(self.rect.y  + 2 * R >= height - border_size - 5):
            PLAY = False
            player_win = pygame.transform.scale(pygame.image.load('win1.gif'), (int(width / 1.5), int(height / 2.5)))




class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.image.fill(pygame.Color('white'))


class Slider(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, w, h, group):
        super().__init__(all_sprites)
        self.image = pygame.Surface([w, h])
        self.rect = pygame.Rect(x1, y1, w, h)
        pygame.draw.rect(self.image, pygame.Color("white"),
                           (0, 0,  self.image.get_width(), self.image.get_height()), 0)

        self.add(group)

    def go(self, delta):
        if(border_size + 3 < self.rect.x + delta and self.rect.x + delta + self.image.get_width() < width - border_size - 3):
            self.rect.x += delta


class Text_Block(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, s, color, sz):
        super().__init__()
        self.image = pygame.Surface([1600, 200 ])
        self.image.set_alpha(0)
        font = pygame.font.Font(None, sz)
        string_rendered = font.render(s, 1, color)
        self.image = string_rendered
        self.rect = self.image.get_rect()
        self.rect.x = x1 + w_b // 2
        self.rect.y = y1 - 5 + h_b // 2
        self.add(texts)


class score_block(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, w, h, group):
        super().__init__()

        #color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.borders = [Border(x1, y1, x1 + w, y1),
                        Border(x1, y1 + h, x1 + w , y1 + h),
                        Border(x1 , y1 + 1, x1, y1 + h - 1),
                        Border(x1 + w, y1 + 1, x1 + w, y1 + h - 1)]

        self.image = pygame.Surface([w, h])
        self.rect = pygame.Rect(x1, y1, w, h)

        while(pygame.sprite.spritecollideany(self, good_blocks)):
            self.rect.x, self.rect.y =   random.randint(border_size, width - w_b - border_size), random.randint(border_size + 200,
                                                                           height - h_b - border_size - 200)


        self.text_color = pygame.Color('black')
        self.cnt = random.randint(1, 5)
        self.text_block = Text_Block(self.rect.x, self.rect.y, str(self.cnt), self.text_color, FONT_SIZE)


        colors = ['#00FF00', '#00FFFF', '#FF00FF', '#FFFF00', '#FFA07A']
        self.color = pygame.Color(random.choice(colors))
        pygame.draw.rect(self.image, self.color,
                           (0, 0,  self.image.get_width(), self.image.get_height()), 0)


        self.add(group)
    def update(self):
        if self.cnt == 0:
            for i in self.borders:
                i.kill()
            self.text_block.kill()
            self.kill()

    def change_text(self):
            self.text_block.kill()
            self.text_block =  Text_Block(self.rect.x, self.rect.y, str(self.cnt), self.text_color, FONT_SIZE)


my = Ball(R, 300, 300, balls_sprites)
#Ball(R, 400, 400, balls_sprites)

Border(border_size, border_size, width - border_size, border_size)
Border(border_size, height - border_size, width - border_size, height - border_size)
Border(border_size, border_size, border_size, height - border_size)
Border(width - border_size, border_size, width - border_size, height - border_size)




for _ in range(20):
    score_block(random.randint(border_size, width - w_b - border_size), random.randint(border_size + 200,
                                                                           height - h_b - border_size - 200), w_b, h_b, good_blocks)




my_block1 = Slider(width // 2, height - h - 10,  w, h, horizontal_borders)
my_block2 = Slider(width // 2, 10,  w, h, horizontal_borders)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == MYEVENTTYPE:
            if ball_speed + delta <= 15:
                ball_speed += delta
                if my.vx > 0:
                    my.vx = ball_speed
                else:
                    my.vy = -ball_speed

                if my.vy > 0:
                    my.vy = ball_speed
                else:
                    my.vy = -ball_speed




        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                motion1 += -speed
            if event.key == pygame.K_RIGHT:
                motion1 += speed

            if event.key == pygame.K_a:
                motion2 += -speed
            if event.key == pygame.K_d:
                motion2 += speed

            if event.key == pygame.K_f:
                restart()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                motion1 += speed
            if event.key == pygame.K_RIGHT:
                motion1 += -speed

            if event.key == pygame.K_a:
                motion2 += speed
            if event.key == pygame.K_d:
                motion2 += -speed


    if(PLAY):
        fon.draw(screen)
        balls_sprites.update()
        good_blocks.update()
        my_block1.go(motion1)
        my_block2.go(motion2)
        walls_sprites.draw(screen)
        all_sprites.draw(screen)
        good_blocks.draw(screen)
        balls_sprites.draw(screen)
        texts.draw(screen)
        pygame.display.flip()
        clock.tick(160)
    else:
        fon.draw(screen)
        screen.blit(player_win, (int(width // 6), height // 3))
        pygame.display.flip()

pygame.quit()
