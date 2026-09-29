import pygame
import asyncio

pygame.init()

WIDTH = 800
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Claude Platformer")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

player_image = pygame.image.load("assets/sprite.png").convert_alpha()
token_image = pygame.image.load("assets/token.png").convert_alpha()

player_image = pygame.transform.scale(player_image, (40, 40))
token_image = pygame.transform.scale(token_image, (25, 25))

player = pygame.Rect(100, 400, 40, 40)
player_x = 100
player_y = 400

x_speed = 5
y_velocity = 0
gravity = 0.6
jump_power = -11
on_ground = False
jump_grace = 0

max_tokens = 30
tokens = max_tokens
collected = 0

platforms = [
    pygame.Rect(0, 450, 800, 50),
    pygame.Rect(100, 350, 180, 20),
    pygame.Rect(350, 300, 180, 20),
    pygame.Rect(600, 220, 140, 20),
    pygame.Rect(450, 150, 120, 20),
    pygame.Rect(200, 220, 140, 20),
]

token_positions = [
    pygame.Rect(160, 315, 25, 25),
    pygame.Rect(420, 265, 25, 25),
    pygame.Rect(650, 185, 25, 25),
    pygame.Rect(490, 115, 25, 25),
    pygame.Rect(250, 185, 25, 25),
]

distance_moved = 0
won = False
lost = False


def reset_game():
    global player_x, player_y, y_velocity
    global collected, distance_moved, won, lost
    global tokens, max_tokens, jump_grace, on_ground, player

    player_x = 100
    player_y = 400
    y_velocity = 0
    collected = 0
    distance_moved = 0
    won = False
    lost = False
    max_tokens = 30
    tokens = max_tokens
    jump_grace = 0
    on_ground = False
    player = pygame.Rect(100, 400, 40, 40)

    token_positions.clear()
    token_positions.extend([
        pygame.Rect(160, 315, 25, 25),
        pygame.Rect(420, 265, 25, 25),
        pygame.Rect(650, 185, 25, 25),
        pygame.Rect(490, 115, 25, 25),
        pygame.Rect(250, 185, 25, 25),
    ])


async def main():
    global player
    global player_x, player_y, y_velocity
    global on_ground, jump_grace
    global distance_moved
    global tokens, max_tokens
    global collected, won, lost

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    if not won and not lost and tokens > 0:
                        if on_ground or jump_grace > 0:
                            y_velocity = jump_power
                            on_ground = False
                            jump_grace = 0

                if event.key == pygame.K_r and (won or lost):
                    reset_game()

        keys = pygame.key.get_pressed()

        if not won and not lost and tokens > 0:

            dx = 0

            if keys[pygame.K_LEFT]:
                dx = -x_speed

            if keys[pygame.K_RIGHT]:
                dx = x_speed

            old_x = player_x
            player_x += dx

            if player_x < 0:
                player_x = 0

            if player_x > WIDTH - player.width:
                player_x = WIDTH - player.width

            actual_horizontal_movement = abs(player_x - old_x)
            distance_moved += actual_horizontal_movement

            while distance_moved >= 20:
                if tokens > 0:
                    tokens -= 1
                distance_moved -= 20

            y_velocity += gravity
            player_y += y_velocity

            player = pygame.Rect(
                int(player_x),
                int(player_y),
                40,
                40
            )

            on_ground = False

            for platform in platforms:
                if player.colliderect(platform) and y_velocity >= 0:
                    player.bottom = platform.top
                    player_y = player.y
                    y_velocity = 0
                    on_ground = True

            if on_ground:
                jump_grace = 5
            elif jump_grace > 0:
                jump_grace -= 1

            for token in token_positions[:]:
                if player.colliderect(token):
                    token_positions.remove(token)
                    collected += 1
                    tokens += 5
                    max_tokens += 5

            if len(token_positions) == 0:
                won = True

            if tokens <= 0 and not won:
                tokens = 0
                lost = True

        screen.fill((135, 206, 235))

        for platform in platforms:
            pygame.draw.rect(
                screen,
                (80, 180, 80),
                platform
            )

        for token in token_positions:
            screen.blit(token_image, token)

        screen.blit(player_image, player)

        token_text = font.render(
            f"Movement tokens: {tokens}",
            True,
            (0, 0, 0)
        )

        collected_text = font.render(
            f"Collected: {collected}/5",
            True,
            (0, 0, 0)
        )

        screen.blit(token_text, (20, 20))
        screen.blit(collected_text, (20, 55))

        if won:
            win_text = font.render(
                f"You won! Max tokens: {max_tokens}. Press R to play again.",
                True,
                (0, 0, 0),
            )
            screen.blit(win_text, (130, 80))

        if lost:
            lose_text = font.render(
                "Out of movement tokens. Press R to restart.",
                True,
                (0, 0, 0),
            )
            screen.blit(lose_text, (190, 80))

        pygame.display.flip()

        clock.tick(60)

        await asyncio.sleep(0)


asyncio.run(main())
