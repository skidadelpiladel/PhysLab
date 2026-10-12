import pygame
import pygame_gui

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
manager = pygame_gui.UIManager((800,400))
mass_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(500,50, 250, 25),
    start_value=ball_mass,
    value_range=(0.5, 5.0),
    manager=manager,
)
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if event.type == pygame.gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == mass_slider:
                ball_mass = event.value
import pygame
import pygame_gui

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PhysLab")

clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Simulation settings
ball_x, ball_y = 200.0, 250.0
ball2_x, ball2_y = 600.0, 250.0

ball_speed = 1.0
ball2_speed = -1.0

ball_mass = 1.0
ball2_mass = 2.0

colliding = False
running = True

# UI panel
panel = pygame.Rect(650, 30, 320, 410)

mass1_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(20, 30, 270, 30),
    text="Blue mass: 1.0 kg",
    manager=manager,
)

mass1_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(20, 65, 270, 25),
    start_value=1.0,
    value_range=(0.5, 5.0),
    manager=manager,
)

mass2_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(20, 115, 270, 30),
    text="Orange mass: 2.0 kg",
    manager=manager,
)

mass2_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(20, 150, 270, 25),
    start_value=2.0,
    value_range=(0.5, 5.0),
    manager=manager,
)

info_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(20, 205, 290, 70),
    text="Adjust masses to change collisions.",
    manager=manager,
)

reset_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(20, 300, 270, 40),
    text="Reset simulation",
    manager=manager,
)

font = pygame.font.Font(None, 26)
small_font = pygame.font.Font(None, 22)

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == mass1_slider:
                ball_mass = event.value
                mass1_label.set_text(
                    f"Blue mass: {ball_mass:.1f} kg"
                )

            elif event.ui_element == mass2_slider:
                ball2_mass = event.value
                mass2_label.set_text(
                    f"Orange mass: {ball2_mass:.1f} kg"
                )

        if (
            event.type == pygame_gui.UI_BUTTON_PRESSED
            and event.ui_element == reset_button
        ):
            ball_x, ball_y = 200.0, 250.0
            ball2_x, ball2_y = 600.0, 250.0
            ball_speed = 1.0
            ball2_speed = -1.0
            colliding = False

    # Move balls
    ball_x += ball_speed
    ball2_x += ball2_speed

    # Wall bounces preserve each ball's speed magnitude
    if ball_x >= 630:
        ball_x = 630
        ball_speed = -abs(ball_speed)
    elif ball_x <= 20:
        ball_x = 20
        ball_speed = abs(ball_speed)

    if ball2_x >= 630:
        ball2_x = 630
        ball2_speed = -abs(ball2_speed)
    elif ball2_x <= 20:
        ball2_x = 20
        ball2_speed = abs(ball2_speed)

    # Collision detection
    distance = abs(ball_x - ball2_x)

    if distance <= 40 and not colliding:
        colliding = True

        old_v1 = ball_speed
        old_v2 = ball2_speed

        momentum_before = (
            ball_mass * old_v1
            + ball2_mass * old_v2
        )

        energy_before = (
            0.5 * ball_mass * old_v1**2
            + 0.5 * ball2_mass * old_v2**2
        )

        total_mass = ball_mass + ball2_mass

        new_v1 = (
            (ball_mass - ball2_mass) / total_mass * old_v1
            + (2 * ball2_mass) / total_mass * old_v2
        )

        new_v2 = (
            (2 * ball_mass) / total_mass * old_v1
            + (ball2_mass - ball_mass) / total_mass * old_v2
        )

        ball_speed = new_v1
        ball2_speed = new_v2

        momentum_after = (
            ball_mass * ball_speed
            + ball2_mass * ball2_speed
        )

        energy_after = (
            0.5 * ball_mass * ball_speed**2
            + 0.5 * ball2_mass * ball2_speed**2
        )

        print(f"Momentum: {momentum_before:.4f} -> {momentum_after:.4f}")
        print(f"Kinetic energy: {energy_before:.4f} -> {energy_after:.4f}")

    elif distance > 40:
        colliding = False

    # Draw scene
    screen.fill((25, 25, 35))

    pygame.draw.circle(
        screen, (80, 180, 255),
        (round(ball_x), round(ball_y)), 20
    )
    pygame.draw.circle(
        screen, (255, 150, 80),
        (round(ball2_x), round(ball2_y)), 20
    )

    pygame.draw.rect(screen, (40, 40, 55), panel, border_radius=12)

    title = font.render("PHYSLAB CONTROLS", True, (240, 240, 255))
    screen.blit(title, (670, 45))

    help_text = small_font.render(
        "Change mass, then observe collisions.",
        True, (200, 200, 215)
    )
    screen.blit(help_text, (670, 90))

    manager.update(time_delta)
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()

                mass_label.set_text(

                )
        
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
        print("collision detected!")

        old_ball_speed = ball_speed
        old_ball2_speed = ball2_speed

        momentum_before=ball_mass*ball_speed + ball2_mass*ball2_speed
        new_ball_speed = ((ball_mass - ball2_mass)/(ball_mass + ball2_mass)*(old_ball_speed))+((2*ball2_mass)/(ball_mass+ball2_mass)*(old_ball2_speed))

        new_ball2_speed = (((2*ball_mass)/(ball_mass+ball2_mass)*(old_ball_speed)))+(((ball2_mass-ball_mass)/(ball_mass+ball2_mass)*(old_ball2_speed)))

        ball_speed = new_ball_speed
        ball2_speed = new_ball2_speed

        momentum_after=ball_mass*ball_speed + ball2_mass*ball2_speed
        
        print("momentum before collision:", momentum_before)
        print("momentum after collision:", momentum_after)

      
      

    elif distance > 40:
        colliding = False
    pygame.draw.circle(screen, (80, 180, 255), (ball_x,ball_y), 20)

    pygame.draw.circle(screen, (255, 150, 80), (ball2_x,ball2_y), 20)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
