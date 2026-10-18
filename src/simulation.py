# pygame collision simulator project 
# ----------------------------------
# Note: I remember that python's float precision sometimes messes up the collision checks,
# but it seems to work fine if we just round things or use small thresholds.
# TODO: maybe add walls that you can move later? Right now they are hardcoded.

import pygame
import pygame_gui

pygame.init()

# screen sizes - kept it a bit wide for the gui stuff on the right
WIDTH = 1100
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PhysLab | Collision Simulator")

clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# stolen some color schemes that i think would look nice for PhysLab
BACKGROUND = (15, 20, 32)
PANEL=(24,32,48)
PANEL_LIGHT=(31,32,61)
BLUE=(65,190,255)
ORANGE=(255,166,91)
WHITE=(235,242,252)
MUTED=(145,160,182)
ACCENT=(80,220,155)
SUCCESS=(80,220,155)
DANGER=(255,100,115)
BORDER=(48,63,86)

# initial ball stuff
ball_x = 200.0
ball_y = 220.0
ball2_x = 500.0
ball2_y = 220.0

ball_speed = 1.0
ball2_speed = -1.0

ball_mass = 1.0
ball2_mass = 2.0

BALL_RADIUS = 20
LEFT_WALL = 40 +BALL_RADIUS
RIGHT_WALL = 700 - BALL_RADIUS # arbitrary boundary where the track ends

colliding = False
running = True
paused=False

# fonts - nothing fancy
font = pygame.font.Font(None, 28)
small_font = pygame.font.Font(None, 23)

# UI elements setup 
# Man, positioning these by hand is always such a pain...
title_label=pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(30,15,500,40),
    text="PHYSLAB|Collision simulator|",
    manager=manager
)

mass1_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(770, 145, 260, 30),
    text="Blue mass: 1.0 kg",
    manager=manager
)

mass1_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(770, 180, 260, 25),
    start_value=ball_mass,
    value_range=(0.5, 5.0),
    manager=manager
)

mass2_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(770, 225, 260, 30),
    text="Orange mass: 2.0 kg",
    manager=manager
)

mass2_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(770, 260, 260, 25),
    start_value=ball2_mass,
    value_range=(0.5, 5.0),
    manager=manager
)

reset_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(770, 320, 260, 45),
    text="Reset",
    manager=manager
)

pause_button=pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(770,380,260,45),
    text="Pause",
    manager=manager
)
controls_label=pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(770, 90, 260,35),
    text="SIMULATION CONTROLS",
    manager=manager
    )


# physics formulas - standard 1D elastic collision stuff from high school physics lol
def calculate_collisions(m1, m2, v1, v2):
    total_mass = m1 + m2
    
    # velocity for ball 1
    new_v1 = (((m1 - m2) / total_mass) * v1) + (((2 * m2) / total_mass) * v2)
    
    # velocity for ball 2
    new_v2 = (((2 * m1) / total_mass) * v1) + (((m2 - m1) / total_mass) * v2)
    
    return new_v1, new_v2


def momentum(m1, m2, v1, v2):
    return (m1 * v1) + (m2 * v2)


def kinetic_energy(m1, m2, v1, v2):
    return (0.5 * m1 * (v1 ** 2)) + (0.5 * m2 * (v2 ** 2))


# helper to draw text easily without writing 3 lines every time
def draw_text(text, x, y, color=WHITE, selected_font=None):
    if selected_font is None:
        selected_font = small_font

    image = selected_font.render(str(text), True, color)
    screen.blit(image, (x, y))


def reset_simulation():
    # gotta use global to modify these values back to start
    global ball_x, ball2_x, ball_speed, ball2_speed, colliding, has_collided
    global momentum_before, momentum_after, energy_before, energy_after

    ball_x = 200.0
    ball2_x = 500.0
    ball_speed = 1.0
    ball2_speed = -1.0
    
    colliding = False
    has_collided = False

    momentum_before = 0.0
    momentum_after = 0.0
    energy_before = 0.0
    energy_after = 0.0


# tracking variables for checks
momentum_before = 0.0
momentum_after = 0.0
energy_before = 0.0
energy_after = 0.0
has_collided = False

# Main Loop

# Main Loop
while running:
    time_delta = clock.tick(60) / 1000.0

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        # Handle slider changes
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == mass1_slider:
                ball_mass = float(event.value)
                mass1_label.set_text(f"Blue mass: {ball_mass:.1f} kg")
            elif event.ui_element == mass2_slider:
                ball2_mass = float(event.value)
                mass2_label.set_text(f"Orange mass: {ball2_mass:.1f} kg")

        # Handle buttons
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == reset_button:
                reset_simulation()
            elif event.ui_element == pause_button:
                paused = not paused

            if event.ui_element == pause_button:
                pause_button.set_text("Resume" if paused else "Pause")

    # Update physics only when not paused
    if not paused:
        # Update positions
        ball_x += ball_speed
        ball2_x += ball2_speed

        # Wall bounces for ball 1
        if ball_x >= RIGHT_WALL:
            ball_x = RIGHT_WALL
            ball_speed = -abs(ball_speed)
        elif ball_x <= LEFT_WALL:
            ball_x = LEFT_WALL
            ball_speed = abs(ball_speed)

        # Wall bounces for ball 2
        if ball2_x >= RIGHT_WALL:
            ball2_x = RIGHT_WALL
            ball2_speed = -abs(ball2_speed)
        elif ball2_x <= LEFT_WALL:
            ball2_x = LEFT_WALL
            ball2_speed = abs(ball2_speed)

        # Check distance between the balls
        distance = abs(ball_x - ball2_x)

        # Calculate relative velocity
        relative_velocity = ball_speed - ball2_speed

        # Check if the balls are approaching each other
        approaching = (
            (ball_x < ball2_x and relative_velocity > 0)
            or (ball_x > ball2_x and relative_velocity < 0)
        )

        if distance <= BALL_RADIUS * 2 and not colliding and approaching:
            colliding = True

            old_v1 = ball_speed
            old_v2 = ball2_speed

            # Calculate momentum and energy before collision
            momentum_before = momentum(ball_mass, ball2_mass, old_v1, old_v2)
            energy_before = kinetic_energy(ball_mass, ball2_mass, old_v1, old_v2)

            # Calculate new velocities
            ball_speed, ball2_speed = calculate_collisions(
                ball_mass, ball2_mass, old_v1, old_v2
            )

            # Calculate momentum and energy after collision
            momentum_after = momentum(ball_mass, ball2_mass, ball_speed, ball2_speed)
            energy_after = kinetic_energy(ball_mass, ball2_mass, ball_speed, ball2_speed)

            has_collided = True
            print("Collision happened!")

        elif distance > BALL_RADIUS * 2:
            colliding = False

    # Draw background (always runs, even while paused)
    screen.fill(BACKGROUND)

    pygame.draw.rect(
        screen, (35, 45, 62),
        pygame.Rect(20, 75, 700, 390),
        border_radius=12
    )
    pygame.draw.rect(
        screen, (45, 58, 78),
        pygame.Rect(740, 75, 340, 390),
        border_radius=12
    )
    pygame.draw.rect(
        screen, (35, 45, 62),
        pygame.Rect(20, 485, 1060, 190),
        border_radius=12
    )

    # Draw track and balls
    pygame.draw.line(screen, (65, 80, 105), (40, ball_y), (700, ball_y), 2)
    pygame.draw.circle(screen, BLUE, (int(ball_x), int(ball_y)), BALL_RADIUS)
    pygame.draw.circle(screen, ORANGE, (int(ball2_x), int(ball2_y)), BALL_RADIUS)

    # Draw simulation information
    draw_text("SIMULATION", 40, 95, MUTED)
    draw_text(f"Blue: {ball_mass:.1f} kg | v = {ball_speed:.3f}", 40, 125, BLUE)
    draw_text(f"Orange: {ball2_mass:.1f} kg | v = {ball2_speed:.3f}", 40, 155, ORANGE)

    # Draw physics validation
    draw_text("PHYSICS VALIDATION", 40, 505, WHITE, font)

    if has_collided:
        draw_text(
            f"Momentum: {momentum_before:.4f} -> {momentum_after:.4f}",
            40, 550
        )
        draw_text(
            f"Kinetic Energy: {energy_before:.4f} -> {energy_after:.4f}",
            40, 580
        )

        momentum_ok = abs(momentum_before - momentum_after) < 0.0001
        energy_ok = abs(energy_before - energy_after) < 0.0001

        if momentum_ok and energy_ok:
            draw_text("Conservation checks passed", 40, 615, (100, 230, 165))
        else:
            draw_text("Conservation checks failed", 40, 615, (255, 100, 100))
    else:
        draw_text("Waiting for collision...", 40, 550, MUTED)

    # Update UI and refresh display
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
