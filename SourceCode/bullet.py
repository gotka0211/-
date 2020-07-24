import pygame
import random as rnd

#클래스 호출시 바로 총알 리스트에 저장
bullets = [] #리스트를 이 파일에 집어넣었습니다.

class Normal:  #일반적인 형태의 총알입니다.
    def __init__(self, x, y, to_x, to_y):
        rcbb1 = rnd.randint(-40,40)  #색깔이 랜덤입니다. (rc = random color)
        rcbb2 = rnd.randint(-40,40)
        self.pos = [x, y]
        self.to = [to_x, to_y]
        self.color = (215+rcbb1, 215+rcbb2, 0)  #노란색을 기본으로 조금씩 색이 다르게 생성됩니다.
        self.speed = 0.5
        #색상에 따라 피해량과 크기가 변합니다.
        if rcbb1+rcbb2 >30:
            self.damage = 25
            self.radius = 7
        elif rcbb1+rcbb2 >-30 :
            self.damage = 17
            self.radius = 5
        else :
            self.damage = 21
            self.radius = 6
        bullets.append(self)
        self.mctt = 1000

    def update_and_draw(self, dt, screen):
        width, height = screen.get_size()
        self.pos[0] = (self.pos[0] + dt * self.to[0] * self.speed) % width
        self.pos[1] = (self.pos[1] + dt * self.to[1] * self.speed) % height
        pos_int = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(screen, self.color, pos_int, self.radius)


#
class big:  #맞으면 즉사하는 총알입니다.
    def __init__(self, x, y, to_x, to_y):
        self.pos = [x, y]
        self.to = [to_x, to_y]
        self.radius = 40
        self.damage = 999999999
        self.speed = 0.2 #대신 좀 느립니다.
        bullets.append(self)
        self.mctt = 200


    def update_and_draw(self, dt, screen):
        width, height = screen.get_size()
        self.pos[0] = (self.pos[0] + dt * self.to[0] * self.speed) % width
        self.pos[1] = (self.pos[1] + dt * self.to[1] * self.speed) % height
        pos_int = (int(self.pos[0]), int(self.pos[1]))
        for i in range(5): #그라데이션을 넣었습니다.
            pygame.draw.circle(screen, (255 - i * 30, 40 * i, 50 * i), pos_int, self.radius - i * 8, 8)

#
class jumsa: #조정간 점사할 때 그 점사 맞습니다. 5발씩 날라오는 총알입니다.
    def __init__(self, x, y, to_x, to_y):
        self.pos = [x, y]
        self.to = [to_x, to_y]
        self.radius = 2
        self.color = (0, 255, 255)
        self.speed = 0.8 #얘는 데미지가 약한대신 빠릅니다.
        self.damage = 8
        bullets.append(self)
        self.mctt = 50 # 발당 데미지는 적지만 총알 갯수가 많이 때문에 피하지않으면 막대한 피해를 입게 됩니다.


    def update_and_draw(self, dt, screen):
        width, height = screen.get_size()
        self.pos[0] = (self.pos[0] + dt * self.to[0] *self.speed ) % width
        self.pos[1] = (self.pos[1] + dt * self.to[1] *self.speed ) % height
        pos_int = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(screen, self.color, pos_int, self.radius)

#
class blackhole:
    def __init__(self, x, y, to_x, to_y):
        self.pos = [x, y]
        self.to = [to_x, to_y]
        self.radius = 30
        self.color = (0, 0, 70) #블랙홀이니 잘 안보여야합니다.
        self.damage = 5
        self.speed = 0.05 # 벗어나지 않으면 체력이 순식간에 줄어들게 됩니다.
        bullets.append(self)
        self.mctt = 15

    def update_and_draw(self, dt, screen):
        width, height = screen.get_size()
        self.pos[0] = (self.pos[0] + dt * self.to[0] * self.speed) % width
        self.pos[1] = (self.pos[1] + dt * self.to[1] * self.speed) % height
        pos_int = (int(self.pos[0]), int(self.pos[1]))
        for i in range(4): # 소용돌이 모양을 만들고 싶었습니다.
            pygame.draw.circle(screen, self.color, pos_int, self.radius - i * 5, 3)
