import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the display
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("AI Assistant Avatar")

# Colors
WHITE = (255, 255, 255)

# States
HAPPY = 'happy'
LISTENING = 'listening'
THINKING = 'thinking'

class AnimeGirl:
    def __init__(self):
        self.current_state = HAPPY
        self.load_images()

    def load_images(self):
        # Using try-except blocks so the code doesn't crash if files are missing
        try:
            self.happy_image = pygame.image.load('happy.png').convert_alpha()
            self.listening_image = pygame.image.load('listening.png').convert_alpha()
            self.thinking_image = pygame.image.load('thinking.png').convert_alpha()
        except pygame.error as e:
            print(f"Error loading images: {e}")
            print("Creating colored placeholder surfaces instead...")
            # Fallbacks if you don't have the image files in your directory yet
            self.happy_image = pygame.Surface((200, 300)); self.happy_image.fill((0, 255, 0)) # Green
            self.listening_image = pygame.Surface((200, 300)); self.listening_image.fill((0, 0, 255)) # Blue
            self.thinking_image = pygame.Surface((200, 300)); self.thinking_image.fill((255, 255, 0)) # Yellow

    def set_state(self, state):
        self.current_state = state

    def draw(self, screen):
        # Pick the active image based on state
        if self.current_state == HAPPY:
            active_image = self.happy_image
        elif self.current_state == LISTENING:
            active_image = self.listening_image
        elif self.current_state == THINKING:
            active_image = self.thinking_image
        else:
            active_image = self.happy_image

        # Properly center the image on the screen
        image_rect = active_image.get_rect()
        image_rect.center = (display_width // 2, display_height // 2)
        
        screen.blit(active_image, image_rect)

# Main game setup
anime_girl = AnimeGirl()
clock = pygame.time.Clock()

# Main loop
while True:
    # Handle inputs/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # TESTING LOGIC: Press keys to switch states manually
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                anime_girl.set_state(HAPPY)
            elif event.key == pygame.K_2:
                anime_girl.set_state(LISTENING)
            elif event.key == pygame.K_3:
                anime_girl.set_state(THINKING)

    # Rendering
    screen.fill(WHITE)        # Fill background
    anime_girl.draw(screen)   # Draw the avatar
    pygame.display.update()   # Refresh screen
    clock.tick(60)            # Limit to 60 Frames Per Second

