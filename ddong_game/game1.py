import pygame
from random import *
####################################################
####################################################
# 기본 초기화 (반드시; 해야 하는 것들)
pygame.init()       # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 480      # 가로크기
screen_height = 640         # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("똥피하기")           # 게임 이름

# FPS (화면 프레임 수)
clock = pygame.time.Clock()
####################################################
####################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)

# 배경 이미지 불러오기
background = pygame.image.load("./background2.png")
 
# 스프라이트(캐릭터) 불러오기
# character = pygame.image.load("/Users/macbookpro/workspace/pygame_basic/character2.png")
character = pygame.image.load("./character2.png")
character_size = character.get_rect().size      # 이미지의 크기를 구해옴
character_width = character_size[0]     # 캐릭터의 가로 크기
character_height = character_size[1]     # 캐릭터의 세로 크기
character_x_pos = screen_width / 2 - character_width / 2     # 화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height    # 화면 세로 크기의 가장 아래에 해당하는 곳에 위치

# 이동할 좌표
to_x = 0
to_y = 0

# 이동속도
character_speed = 0.5
enemy_speed = 5
enemy_speed2 = 4
enemy_speed3 = 3
enemy_speed4 = 6
enemy_speed5 = 7
enemy_speed6 = 8

# 적 enemy 캐릭터   ->  객체? / 클래스?
enemy = pygame.image.load("./enemy1.png")
enemy_size = enemy.get_rect().size      # 이미지의 크기를 구해옴
enemy_width = enemy_size[0]     # 적의 가로 크기
enemy_height = enemy_size[1]     # 적의 세로 크기
enemy_x_pos = randint(0, screen_width-enemy_width)
enemy_y_pos = 0    # 화면 세로 크기의 가장 아래에 해당하는 곳에 위치

enemys = []
enemys2 = []
enemys3 = []
enemys4 = []
enemys5 = []
enemys6 = []

enemy_num = 0
enemy_num2 = 3
enemy_num3 = 6
enemy_num4 = 10
enemy_num5 = 20
enemy_num6 = 30

# 폰트 정의
game_font = pygame.font.Font(None, 40)      # 폰트 객체 생성 (폰트, 크기)

# 총 시간
total_time = 0

# 시작 시간 정보 
start_ticks = pygame.time.get_ticks()       # 시작 tick을 받아옴


# 이벤트 루프 (실행되고 있어야 창이 꺼지지 않음)
running = True      # 게임이 진행중인가?

while running:
    dt = clock.tick(60)         # 게임 화면의 초당 프레임 수를 설정

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():        # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT:         # 창이 닫히는 이벤트가 발생하였는가?
            running = False         # 게임이 진행중이 아님
            
        if event.type == pygame.KEYDOWN:        # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:      # 캐릭터를 왼쪽으로
                to_x -= character_speed   # to_x = to_x -character_speed
            elif event.key == pygame.K_RIGHT:       # 캐릭터를 오른쪽으로
                to_x += character_speed

        if event.type == pygame.KEYUP:      # 방향키를 떼면 멈춤 / for문이기때문에 만약 떼지면 to값을 초기화 처리해줘야 함 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
    
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000       # 경과 시간(ms)을 1000으로 나누어서 초 단위로 표시
   
    # 똥이 여러개 나오도록
    if int(elapsed_time) == int(enemy_num):
        enemys.append([randint(0, screen_width-enemy_width), 0])
        enemy_num += 1
    if int(elapsed_time) >= 3 and int(elapsed_time) == int(enemy_num2):
        enemys2.append([randint(0, screen_width-enemy_width), 0])
        enemy_num2 += 1
    if int(elapsed_time) >= 6 and int(elapsed_time) == int(enemy_num3):
        enemys3.append([randint(0, screen_width-enemy_width), 0])
        enemy_num3 += 1
    if int(elapsed_time) >= 10 and int(elapsed_time) == int(enemy_num4):
        enemys4.append([randint(0, screen_width-enemy_width), 0])
        enemy_num4 += 1
    if int(elapsed_time) >= 20 and int(elapsed_time) == int(enemy_num5):
        enemys5.append([randint(0, screen_width-enemy_width), 0])
        enemy_num5 += 1
    if int(elapsed_time) >= 30 and int(elapsed_time) == int(enemy_num6):
        enemys6.append([randint(0, screen_width-enemy_width), 0])
        enemy_num6 += 1


    # 똥이 내려옴
    enemys = [ [d[0], d[1] + enemy_speed] for d in enemys]
    enemys2 = [ [d[0], d[1] + enemy_speed2] for d in enemys2]
    enemys3 = [ [d[0], d[1] + enemy_speed3] for d in enemys3]
    enemys4 = [ [d[0], d[1] + enemy_speed4] for d in enemys4]
    enemys5 = [ [d[0], d[1] + enemy_speed5] for d in enemys5]
    enemys6 = [ [d[0], d[1] + enemy_speed6] for d in enemys6]

    enemys = [ [ d[0], d[1] ] for d in enemys if d[1] <= screen_height-40]
    enemys2 = [ [ d[0], d[1] ] for d in enemys2 if d[1] <= screen_height-40]
    enemys3 = [ [ d[0], d[1] ] for d in enemys3 if d[1] <= screen_height-40]
    enemys4 = [ [ d[0], d[1] ] for d in enemys4 if d[1] <= screen_height-40]
    enemys5 = [ [ d[0], d[1] ] for d in enemys5 if d[1] <= screen_height-40]
    enemys6 = [ [ d[0], d[1] ] for d in enemys6 if d[1] <= screen_height-40]

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += to_x * dt        # dt를 곱해줌으로 이동속도를 보정

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > (screen_width-character_width):
        character_x_pos = (screen_width-character_width)

    # 4. 충돌 처리
    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos


    # 충돌 체크
    for enemy_x_pos, enemy_y_pos in enemys:
        enemy_rect = enemy.get_rect()
        enemy_rect.left = enemy_x_pos
        enemy_rect.top = enemy_y_pos
        if character_rect.colliderect(enemy_rect):       # 캐릭터가 적과 충돌을 했는가?
            print("똥 맞았당")
            running = False

    for enemy_x_pos, enemy_y_pos in enemys2:
        enemy_rect2 = enemy.get_rect()
        enemy_rect2.left = enemy_x_pos
        enemy_rect2.top = enemy_y_pos
        if character_rect.colliderect(enemy_rect2):       # 캐릭터가 적과 충돌을 했는가?
            print("똥 맞았당")
            running = False

    for enemy_x_pos, enemy_y_pos in enemys3:
        enemy_rect3 = enemy.get_rect()
        enemy_rect3.left = enemy_x_pos
        enemy_rect3.top = enemy_y_pos
        if character_rect.colliderect(enemy_rect3):       # 캐릭터가 적과 충돌을 했는가?
            print("똥 맞았당")
            running = False
    
    for enemy_x_pos, enemy_y_pos in enemys4:
        enemy_rect4 = enemy.get_rect()
        enemy_rect4.left = enemy_x_pos
        enemy_rect4.top = enemy_y_pos
        if character_rect.colliderect(enemy_rect4):       # 캐릭터가 적과 충돌을 했는가?
            print("똥 맞았당")

    for enemy_x_pos, enemy_y_pos in enemys5:
        enemy_rect5 = enemy.get_rect()
        enemy_rect5.left = enemy_x_pos
        enemy_rect5.top = enemy_y_pos
        if character_rect.colliderect(enemy_rect5):       # 캐릭터가 적과 충돌을 했는가?
            print("똥 맞았당")
            running = False

    for enemy_x_pos, enemy_y_pos in enemys6:
        enemy_rect6 = enemy.get_rect()
        enemy_rect6.left = enemy_x_pos
        enemy_rect6.top = enemy_y_pos
        if character_rect.colliderect(enemy_rect6):       # 캐릭터가 적과 충돌을 했는가?
            print("똥 맞았당")
            running = False


    # 5. 화면에 그리기
    screen.blit(background, (0, 0))     # 화면 적용 (배경 그리기)

    screen.blit(character, (character_x_pos, character_y_pos))      # 캐릭터 그리기


    for enemy_x_pos, enemy_y_pos in enemys:
        screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    for enemy_x_pos, enemy_y_pos in enemys2:
        screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    for enemy_x_pos, enemy_y_pos in enemys3:
        screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    for enemy_x_pos, enemy_y_pos in enemys4:
        screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    for enemy_x_pos, enemy_y_pos in enemys5:
        screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    for enemy_x_pos, enemy_y_pos in enemys6:
        screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    # 경과 시간 계산
    timer = game_font.render(str(int(total_time + elapsed_time)), True, (0, 0, 0))        # (출력할 글자, True, 글자 색상)

    screen.blit(timer, (10,10))


    pygame.display.update()         # 게임 화면을 다시 그리기(반드시 계속 호출되어야 함)

game_over = game_font.render("game over", True, (0, 0, 0))
rank = game_font.render("record : " + str(int(elapsed_time)), True, (0, 0, 0))
screen.blit(game_over, (170,200))
screen.blit(rank, (170,250))

pygame.display.update()         # 게임 화면을 다시 그리기(반드시 계속 호출되어야 함)

# 잠시 대기
pygame.time.delay(2000)     # 2초 정도 대기 (ms)


# pygame 종료
pygame.quit()




