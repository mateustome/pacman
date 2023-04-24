import pygame
import sys

def menu_selection():
    # Constants
    WIDTH = 640
    HEIGHT = 480
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    #MAPS = ["Mapa mini", "Iniciar jogo", "Mapa grande"]  # List of available maps
    MAPS = ["Iniciar jogo"] 

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Selecione seu mapa")

    # Load Fonts
    font_title = pygame.font.Font("fonts/Roboto-Regular.ttf", 48)
    font_map = pygame.font.Font("fonts/Roboto-Regular.ttf", 36)

    # Load Background Image
    background = pygame.image.load("images/background.gif")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Main Loop
    while True:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))  # Draw background image
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for i, map_name in enumerate(MAPS):
            # Render Map Names as Buttons
            map_button = font_map.render(map_name, True, WHITE)
            map_button_rect = map_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))

            # Add Hover Effect
            if map_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, GRAY, map_button_rect, border_radius=5)
            else:
                pygame.draw.rect(screen, BLACK, map_button_rect, border_radius=5)
            pygame.draw.rect(screen, WHITE, map_button_rect, 2, border_radius=5)
            screen.blit(map_button, map_button_rect)

            # Check for Mouse Click on Map Buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if map_button_rect.collidepoint(pygame.mouse.get_pos()):
                    print(f"Selected Map: {map_name}")
                    print(f"Selected Map: {i}")
                    return map_name;
                    # Add logic to launch selected map here

        pygame.display.flip()
