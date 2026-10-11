import pygame

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("PhysLab")

ball_x=200
ball_y=200
ball_speed = 1
ball2_x=600
ball2_y=200
ball2_speed= -1
running = True
colliding = False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill((25, 25, 35))

    ball_x += ball_speed

    if ball_x >= 780:
        ball_x = 780
        ball_speed = -1
    elif ball_x <= 20:
        ball_x = 20
        ball_speed = 1

    ball2_x += ball2_speed

    if ball2_x >= 780:
        ball2_x =780
        ball2_speed= -1
    elif ball2_x <= 20:
        ball2_x = 20
        ball2_speed = 1

    distance = abs(ball_x - ball2_x)

    if distance <= 40 and not colliding:
        colliding = True
        ball_speed = 0
        ball2_speed = 0
        print("collision detected!")
    pygame.draw.circle(screen, (80, 180, 255), (ball_x,ball_y), 20)

    pygame.draw.circle(screen, (255, 150, 80), (ball2_x,ball2_y), 20)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
