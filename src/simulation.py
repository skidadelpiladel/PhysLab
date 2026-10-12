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
ball_mass=1
ball2_mass=2
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
        ball_speed = abs(ball_speed)
    elif ball_x <= 20:
        ball_x = 20
        ball_speed = abs(ball_speed)

    ball2_x += ball2_speed

    if ball2_x >= 780:
        ball2_x =780
        ball2_speed= abs(ball2_speed)
    elif ball2_x <= 20:
        ball2_x = 20
        ball2_speed = abs(ball2_speed)

    distance = abs(ball_x - ball2_x)

    if distance <= 40 and not colliding:
        colliding = True
        print("collision detected!")

        old_ball_speed = ball_speed
        old_ball2_speed = ball2_speed

        momentum_before=ball_mass*ball_speed + ball2_mass*ball2_speed
        new_ball_speed = ((ball_mass - ball2_mass)/(ball_mass + ball2_mass)*(old_ball_speed))+((2*ball2_mass)/(ball_mass+ball2_mass)*(old_ball2_speed))
        new_ball2_speed = ((2 * ball_mass / (ball_mass + ball2_mass) * old_ball_speed)+ ((ball2_mass - ball_mass) / (ball_mass + ball2_mass) * old_ball2_speed))

        ball_speed = new_ball_speed
        ball2_speed = new_ball2_speed

        momentum_after=(ball_mass*ball_speed + ball2_mass*ball2_speed)
        
        print("momentum before collision:", momentum_before)
        print("momentum after collision:", momentum_after)

      
      

    elif distance > 40:
        colliding = False
    pygame.draw.circle(screen, (80, 180, 255), (ball_x,ball_y), 20)

    pygame.draw.circle(screen, (255, 150, 80), (ball2_x,ball2_y), 20)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
