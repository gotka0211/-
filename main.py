import pygame
from object import *
import random as rnd
from bullet import *
import math
import time
from datetime import datetime

#충돌감지 함수
def collision(obj1, obj2):
    if math.sqrt((obj1.pos[0] - obj2.pos[0]) ** 2 + (obj1.pos[1] - obj2.pos[1]) ** 2)\
            < obj1.image.get_width()/2 + obj2.radius: # 플레이어와 총알 반지름 크기 반영
        return True
    return False
# 텍스트 출력 함수
def draw_text(txt, size, pos, color):
    font = pygame.font.Font('freesansbold.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, (int(pos[0]), int(pos[1])))

#텍스트 파일에 score를 저장한다음 sort하여 10개의 리스트 까지만 저장후 읽기
def rank_save(playerscore,rank):
    #파일에서 데이터를 한 줄 씩 읽어 랭크리스트에 저장
    with open('rank.txt','r') as f:
        for ff in f.readlines():
            try:
                ff0,ff1 = ff.rstrip().split(',')
                rank.append([ff0, ff1])
            except : pass #기록이 없는 줄이 있을 때(기록이 하나도 없을때), 패스(예외처리)
    #현재 기록 또한 랭크리스트에 저장
    date, score = playerscore.rstrip().split(',')
    rank.append([date, score])
    # 현재 기록이 포함된 랭크리스트를 점수 순으로 정렬 후 파일에 저장
    rank = sorted(rank,key=lambda x:float(x[1]),reverse=True)[:10]
    with open('rank.txt','w') as f:
        for i in rank:
            f.write('{},{}\n'.format(i[0],i[1]))

# 게임 시작
pygame.init()
# 화면설정
pygame.display.set_caption('총알피하기 20163199 김중현')
width, height = 1100, 650   #권장 크기입니다 ㅎㅎ
screen = pygame.display.set_mode((width, height))

# 음향효과
pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

pung = pygame.mixer.Sound('pung.wav')   #폭발사운드
pung.set_volume(0.2)

pigyuck = pygame.mixer.Sound('pigyuck.wav') #피격사운드
pigyuck.set_volume(0.1)

# fps 설정
clock = pygame.time.Clock()
FPS = 70

# 객체 생성
player = Player(width / 2, height / 2) #플레이어 화면 중앙에 생성
bg = Bg(-500, -300) #배경생성
pg = Pg(0,0)  # 피격 효과 불러 놓기 pg = pigyuck
for i in range(10):#게임 시작 시 총알 기본으로 생성
    Normal(0, rnd.random() * height, rnd.random() - 0.5, rnd.random() - 0.5)
time_for_adding_bullets = 0 #총알 생성을 위한 타이머
# 점수저장
start_time = time.time()
score = 0 #시간만 측정
playerscore = 0 #날짜까지 담은 플레이어 기록
rank=[] #기록을 저장하는 리스트
justone = False # 사망시 딱한번 실행하기 위한 변수

# 실행동안(종료버튼 누르기 전까지)
running = True
while running:

    dt = clock.tick(FPS)

    for event in pygame.event.get():
        # 종료버튼 누르면,
        if event.type == pygame.QUIT:
            running = False

            #살아있을 때 플레이어 조작
        if  player.hp >0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.goto(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.goto(1, 0)
                elif event.key == pygame.K_UP:
                    player.goto(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.goto(0, 1)
            # 키를 떼면,
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_LEFT:
                    player.goto(1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.goto(-1, 0)
                elif event.key == pygame.K_UP:
                    player.goto(0, 1)
                elif event.key == pygame.K_DOWN:
                    player.goto(0, -1)

    # 화면 채우기
    bg.update_and_draw(dt, screen, player)
    # 충돌 이펙트 (불꽃과 피해량표시)
    if pg.ct > 0: #pg.ct가 활성화 돼있을때,
        pg.update_and_draw(dt, screen, player)
        draw_text(str(phr), 30, (player.pos[0] + rnd.randint(-30, -10),
                                 player.pos[1] + rnd.randint(-70, -60)), (255, 0, 0))  # 난수는 역동감을 위해섭니다 ㅎㅎ
    # 총알 업데이트
    for b in bullets:  # bullets는 bullet.py에서 불러온 리스트입니다.
        b.update_and_draw(dt, screen)
    # 플레이어 업데이트
    player.update(dt, screen)
    player.draw(screen)

    #플레이어가 살아있을때,
    if player.hp>0:
        # 총알 생성
        time_for_adding_bullets += dt
        if time_for_adding_bullets > 2000: #총알을 2초에 한번씩 생성합니다.
            bbb = rnd.randint(1, 20) #어떤 총알을 새롭게 생성할지 랜덤으로 정하는 변수 bbb = bullet bbobgi (교수님의 커피추첨에서 영감을 얻었습니다.ㅎㅎ)
            if bbb <= 4: #20 %
                big(0, rnd.random() * height, rnd.random() - 0.5, rnd.random() - 0.5)
            elif bbb >= 16: #20%
                ypos = rnd.random() * height  #랜덤으로 뽑아낸 총알 생성위치와 총알 속도를 고정시켜,
                xto, yto = rnd.random() - 0.5, rnd.random() - 0.5
                for i in range (5):  #연달아 일직선으로 향하는 '점사'라는 총알을 생성합니다.
                    jumsa(0+xto*i*40, ypos+yto*i*40, xto, yto)
            elif bbb <= 8: #20%
                blackhole(rnd.random() * width, rnd.random() * height, rnd.random() - 0.5, rnd.random() - 0.5)
            else: # 40%
                Normal(0, rnd.random() * height, rnd.random() - 0.5, rnd.random() - 0.5)
            time_for_adding_bullets -= 2000

        # 충돌 감지
        for b in bullets:
            if collision(player, b) and not player.mujuck: #플레이어가 무적이 아닐때 충돌이면,
                pygame.mixer.Sound.play(pigyuck) #맞는 소리
                player.hp -= b.damage #체력 감소
                phr = b.damage #피해량 표시 (pihaeryang)
                screen.fill((255, 0, 0)) #빨간화면 (타격감 ㅎㅎ)
                pg.ct = 200 #충돌이펙트 지속시간
                player.mct = b.mctt #플레이어 무적시간 부여 , 총알의 종류마다 플레이어의 무적시간이 다릅니다.

        # 무적 활성화
        if player.mct>0:
            player.mujuck = True
        else: # 시간이 지나면 무적이 꺼짐.
            player.mujuck = False

        # 상태창
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, 40))
        pygame.draw.line(screen, (255, 255, 255), (0, 40), (width, 40), 2)
        # 피격시 줄어든 체력 강조
        if pg.ct > 0:
            pygame.draw.line(screen, (255, 0, 0), (400, 20), (900 - (100 - player.hp) * 5 + phr * 5, 20), 25)
        if player.hp <0: player.hp = 0  #hp가 0이하가 돼 RGB값 설정에 생길 수 있는 문제를 막아줍니다.
        #체력에 따라 게이지의 색상이 달라집니다.
        pygame.draw.line(screen, (int(255 * (100 - player.hp) / 100), int(255 * (player.hp) / 100), 0), (400, 20),
                         (900 - (100 - player.hp) * 5, 20), 25)
        # 남은 체력 표시
        hptxt = 'HP : {}'.format(player.hp)
        draw_text(hptxt, 15, (910, 10), (255, 255, 255))
        # score
        score = time.time() - start_time
        txt = 'SCORE: {:.2f}  Bullets: {}'.format(score, len(bullets))
        draw_text(txt, 25, (10, 10), (255, 255, 255))

    # 체력이 0이하면,
    else:
        #  딱 한번 점수 저장 (날짜, 점수)
        if justone == False:
            playerscore = str(datetime.today())[:19] + ',' + str(score)
            print(playerscore)
            rank_save(playerscore, rank)
            #터지는 소리도 딱한번
            pygame.mixer.Sound.play(pung)
            justone = True
        # 사망후 객체들 이동 중지
        player.to = [0, 0]
        bg.to = [0, 0]
        for b in bullets:
            b.to = [0,0]

        #게임오버 메세지와 현재 기록 출력
        draw_text('GAME OVER', 80, (width / 2 - 270, height / 2 - 200), (255, 255, 255))
        txt = 'SCORE: {:.3f} / Bullets: {}'.format(score, len(bullets))
        draw_text(txt, 30, (width / 2 - 220, height / 2 - 100), (255, 255, 255))
        # 기록 출력 인터페이스
        draw_text('---------------| RANK |---------------',25,(width /2 -200,height /2-50),(255,255,0))
        draw_text('NO.  SCORE.                  DATE.', 15, (width / 2 - 200, height / 2 - 20), (150, 150, 0))
        # 저장된 기록들 정렬
        rank = sorted(rank, key=lambda x: float(x[1]), reverse=True)[:10]
        # 저장된 기록들 출력
        for i in range(len(rank)):
            r_txt = ' {0}.  {1:.3f} ({2})'.format(i+1,float(rank[i][1]),rank[i][0])
            # 현재 점수가 등수안에 있는지 확인
            if rank[i][0]+','+rank[i][1] == playerscore: #있으면 하이라이트,
                highlight =(255,255,0)
                draw_text('YOUR SCORE -->', 12, (width / 2 - 300, height / 2 +4+ 25 * i), highlight)
            else :
                highlight = (255,255,255) #없으면 기본 색(흰색)
            # 가독성을 위한 검은 막대기 추가
            pygame.draw.line(screen, (0, 0, 0), (int(width / 2 - 200), int(height / 2 +10+ 25 * i)),
                             (int(width / 2 + 150), int(height / 2 +10+ 25 * i)), 20)
            # 그위에 등수/점수/날짜 출력
            draw_text(r_txt,20,(width /2 -200,height /2 +25*i),highlight)

    # 화면 갱신
    pygame.display.update()
