import pygame

class Player:
    def __init__(self, x, y):
        #현재 이미지
        self.image = pygame.image.load('player.png')
        #체력별 이미지
        self.php100 = pygame.image.load('player.png') #기본이미지
        self.php50 = pygame.image.load('php50.png')  #체력 50이하
        self.php20 = pygame.image.load('php20.png')  #체력 20이하
        #무적일 때 반짝거림을 연출하기 위함 (m = mujuck)
        self.m_image = pygame.image.load('mujuck.png')
        #image가 바뀔 때 원래의 형태를 일시적으로 저장해놓음
        self.temp_image = pygame.image.load('player.png')
        #hp <=0 일때 본체 폭발
        self.die_image = pygame.image.load('die.png')
        self.die_image = pygame.transform.scale(self.die_image, (150, 100))
        #
        self.pos = [x, y]  # 위치
        self.to = [0, 0]  # 방향
        self.angle = 0  #각도
        #
        self.hp = 100  # 체력
        self.mujuck = False #피격시 무적상태 돌입
        self.bbjj = 0  # 무적시 반짝거림 딜레이 (bbanjjack)
        self.mct = 0    #무적지속시간(mujcuk continuing time)

    # 플레이어 이동
    def goto(self, x, y):
        self.to[0] += x
        self.to[1] += y

    #플레이어 이미지 갱신
    def update(self, dt, screen):
        width, height = screen.get_size()
        # 이동 (현위치 + 방향*속도)
        self.pos[0] = self.pos[0] + dt * self.to[0] * 0.5
        self.pos[1] = self.pos[1] + dt * self.to[1] * 0.5
        # 화면 경계 설정
        self.pos[0] = min(max(self.pos[0], self.image.get_width() / 2), width - self.image.get_width() / 2)
        self.pos[1] = min(max(self.pos[1], 40+self.image.get_height() / 2), height - self.image.get_height() / 2)

        #(피격시) 무적상태일 때,
        if self.mujuck:
            self.mct -= dt  #무적지속시간 카운트 (총알종류마다 지속시간이 다름)
            self.bbjj += dt #반짝거림 딜레이(프레임단위로)
            #꺼짐상태와 켜짐상태를 한 세트로 반복
            if self.bbjj <= 3 * dt:
                self.image = self.m_image
                self.image = pygame.transform.scale(self.image, (30, 30))
            elif self.bbjj <= 10 * dt:
                self.image = self.temp_image
                self.image = pygame.transform.scale(self.image, (30, 30))
                self.bbjj = 0
        else: #무적이 아니면,
            if self.hp <= 20: #체력이 20이하일때,
                self.image = self.php20
            elif self.hp <= 50: #체력이 50이하일때,
                self.image = self.php50
            else: #그 외일때,
                self.image = self.php100
            self.temp_image = self.image
            self.image = pygame.transform.scale(self.image, (30, 30))
        # 체력에 따라 플레이어 이미지가 변합니다.
        # 그리고 사망 시 폭발이미지 적용
        if self.hp <= 0:
            self.image = self.die_image


    #갱신된 이미지를 화면에 출력
    def draw(self, screen):
        #본체 방향에 맞게 이미지 회전
        if self.to == [-1, -1]:
            self.angle = 45
        elif self.to == [-1, 0]:
            self.angle = 90
        elif self.to == [-1, 1]:
            self.angle = 135
        elif self.to == [0, 1]:
            self.angle = 180
        elif self.to == [1, 1]:
            self.angle = -135
        elif self.to == [1, 0]:
            self.angle = -90
        elif self.to == [1, -1]:
            self.angle = -45
        elif self.to == [0, -1]:
            self.angle = 0

        rotated = pygame.transform.rotate(self.image, self.angle)
        calib_pos = (self.pos[0] - rotated.get_width() / 2, self.pos[1] - rotated.get_height() / 2)  # 정 중앙에 위치시키기 위함
        screen.blit(rotated, calib_pos)  # 객체 그리기

#충돌 이펙트
class Pg:#pg = pigyuck(피격)
    def __init__(self,x,y):
        self.image = pygame.image.load('pigyuck.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.pos = [x,y]
        self.ct = 0

    def update_and_draw(self, dt, screen,player): #플레이어 위치에 생성됩니다.
        self.ct -= dt #업데이트 마다 지속시간을 깎습니다.
        self.pos[0] = player.pos[0]
        self.pos[1] = player.pos[1]
        calib_pos = (int(self.pos[0] - self.image.get_width() / 2), int(self.pos[1] - self.image.get_height() / 2)) #정중앙에 위치하기 위함
        screen.blit(self.image, calib_pos)

#배경
class Bg:
    def __init__(self, x, y):
        self.image = pygame.image.load('bg.jpg')
        self.pos = [x, y]

    def update_and_draw(self, dt, screen,player):
        #플레이어의 움직임에 영향을 받습니다.
        self.pos[0] = self.pos[0] -1*(player.to[0]*dt*0.03)
        self.pos[1] = self.pos[1] -1*(player.to[1]*dt*0.03 )
        #배경 경계 설정
        self.pos[0] = min(max(self.pos[0],-900), 0)
        self.pos[1] = min(max(self.pos[1],-700), 0 )

        screen.blit(self.image, self.pos)
