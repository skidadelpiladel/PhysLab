import pygame

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("PhysLab")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = false
        
    screen.fill((25, 25, 35))

    ball_x=200
    ball_y=200
    
    pygame.draw.circle(screen, (80, 180, 255), (ball_x,ball_y), 20)
    
    pygame.display.flip()

pygame.quit()
