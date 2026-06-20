import pygame
import sys
import threading
import time
import speech_recognition as sr

# --- PYGAME CONFIGURATION ---
pygame.init()
display_width, display_height = 800, 600
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("AI Companion")

# Color constants
WHITE = (255, 255, 255)

# Visual States
HAPPY = 'happy'
LISTENING = 'listening'
THINKING = 'thinking'

class AnimeAvatar:
    def __init__(self):
        self.current_state = HAPPY
        self.load_assets()

    def load_assets(self):
        """Loads assets or generates colored placeholders if files are missing."""
        try:
            self.images = {
                HAPPY: pygame.image.load('happy.png').convert_alpha(),
                LISTENING: pygame.image.load('listening.png').convert_alpha(),
                THINKING: pygame.image.load('thinking.png').convert_alpha()
            }
        except pygame.error:
            print("Image files not found. Using colored placeholders...")
            # Fallbacks: Green for Happy, Blue for Listening, Yellow for Thinking
            self.images = {
                HAPPY: pygame.Surface((200, 300)),
                LISTENING: pygame.Surface((200, 300)),
                THINKING: pygame.Surface((200, 300))
            }
            self.images[HAPPY].fill((0, 255, 0))
            self.images[LISTENING].fill((0, 0, 255))
            self.images[THINKING].fill((255, 255, 0))

    def set_state(self, state):
        self.current_state = state

    def draw(self, surface):
        active_image = self.images.get(self.current_state, self.images[HAPPY])
        rect = active_image.get_rect(center=(display_width // 2, display_height // 2))
        surface.blit(active_image, rect)

avatar = AnimeAvatar()

# --- VOICE ASSISTANT BACKGROUND WORKER ---
def voice_assistant_worker():
    """Runs continuously in the background, updating the avatar state based on audio."""
    r = sr.Recognizer()
    
    # Allow the Pygame window a moment to initialize completely
    time.sleep(2)
    print("[System Online]")

    while True:
        try:
            with sr.Microphone() as source:
                # 1. Update visual state to Listening
                avatar.set_state(LISTENING)
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("[Listening...]")
                audio = r.listen(source, phrase_time_limit=5)

            # 2. Update visual state to Thinking
            avatar.set_state(THINKING)
            print("[Processing...]")
            query = r.recognize_google(audio).lower()
            print(f"User said: {query}")

            # 3. Handle commands (Expand this section for custom logic)
            if "hello" in query:
                print("Response: Hello! How can I help you?")
            elif "time" in query:
                current_time = time.strftime("%I:%M %p")
                print(f"Response: The current time is {current_time}")
            elif "stop" in query or "quit" in query:
                print("Response: Goodbye!")
                avatar.set_state(HAPPY)
                break
                
            # Reset back to happy/idle state after handling
            avatar.set_state(HAPPY)
            time.sleep(1) 
            
        except sr.UnknownValueError:
            # If microphone audio wasn't clear enough to parse
            avatar.set_state(HAPPY)
        except Exception as e:
            print(f"Error in voice thread: {e}")
            avatar.set_state(HAPPY)
            time.sleep(2)

# Start the voice logic thread smoothly in the background
assistant_thread = threading.Thread(target=voice_assistant_worker, daemon=True)
assistant_thread.start()

# --- MAIN GRAPHICS LOOP ---
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear screen and draw the updated avatar state
    screen.fill(WHITE)
    avatar.draw(screen)
    pygame.display.update()
    
    # Cap framerate to keep CPU usage low on mobile devices
    clock.tick(30)
