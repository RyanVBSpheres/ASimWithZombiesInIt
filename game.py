"""
Graphical zombie survival game using pygame.
"""
import pygame
import sys
import math
from simulation import ZombieSimulation


class ZombieGame:
    """Graphical game interface for the zombie simulation."""
    
    # Movement constant
    DIAGONAL_MOVEMENT_FACTOR = 1 / math.sqrt(2)  # Normalize diagonal movement
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        
        # Window settings
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("A Sim With Zombies In It")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (128, 128, 128)
        self.DARK_GREEN = (0, 128, 0)
        
        # Game settings
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.running = True
        
        # Camera settings (for centering view on player)
        self.camera_x = 0
        self.camera_y = 0
        
        # Scale factor (pixels per game unit)
        self.scale = 20
        
        # Font for UI
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Initialize simulation
        self.sim = ZombieSimulation()
        
        # Player movement state
        self.keys_pressed = set()
        
    def world_to_screen(self, x, y):
        """Convert world coordinates to screen coordinates."""
        screen_x = int((x - self.camera_x) * self.scale + self.width / 2)
        screen_y = int((y - self.camera_y) * self.scale + self.height / 2)
        return screen_x, screen_y
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                self.keys_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
    
    def update(self):
        """Update game state."""
        # Handle player movement
        dx, dy = 0, 0
        
        if pygame.K_w in self.keys_pressed or pygame.K_UP in self.keys_pressed:
            dy = -1
        if pygame.K_s in self.keys_pressed or pygame.K_DOWN in self.keys_pressed:
            dy = 1
        if pygame.K_a in self.keys_pressed or pygame.K_LEFT in self.keys_pressed:
            dx = -1
        if pygame.K_d in self.keys_pressed or pygame.K_RIGHT in self.keys_pressed:
            dx = 1
        
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= self.DIAGONAL_MOVEMENT_FACTOR
            dy *= self.DIAGONAL_MOVEMENT_FACTOR
        
        # Move player if any input
        if dx != 0 or dy != 0:
            self.sim.move_player(dx, dy)
        
        # Update simulation
        self.sim.update()
        
        # Update camera to follow player
        self.camera_x = self.sim.player.x
        self.camera_y = self.sim.player.y
    
    def draw_trail(self, trail, color, max_distance):
        """Draw a single trail point."""
        # Calculate alpha based on intensity
        alpha = min(255, int(trail.intensity * 100))
        if alpha > 0:
            screen_x, screen_y = self.world_to_screen(trail.x, trail.y)
            
            # Draw circle with transparency
            surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*color, alpha), (10, 10), 8)
            self.screen.blit(surface, (screen_x - 10, screen_y - 10))
    
    def draw(self):
        """Draw the game state."""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw smell trails (green)
        for trail in self.sim.trail_system.smell_trails:
            self.draw_trail(trail, self.DARK_GREEN, 20)
        
        # Draw sound trails (blue)
        for trail in self.sim.trail_system.sound_trails:
            self.draw_trail(trail, self.BLUE, 10)
        
        # Draw zombies
        for zombie in self.sim.zombies:
            if zombie.is_alive():
                screen_x, screen_y = self.world_to_screen(zombie.x, zombie.y)
                pygame.draw.circle(self.screen, self.RED, (screen_x, screen_y), 10)
                
                # Draw health bar
                health_ratio = zombie.health / zombie.max_health
                health_width = 20
                pygame.draw.rect(self.screen, self.GRAY, 
                               (screen_x - 10, screen_y - 20, health_width, 4))
                pygame.draw.rect(self.screen, self.GREEN, 
                               (screen_x - 10, screen_y - 20, int(health_width * health_ratio), 4))
        
        # Draw player
        player = self.sim.player
        screen_x, screen_y = self.world_to_screen(player.x, player.y)
        pygame.draw.circle(self.screen, self.YELLOW, (screen_x, screen_y), 12)
        
        # Draw player health bar
        health_ratio = player.health / player.max_health
        health_width = 30
        pygame.draw.rect(self.screen, self.GRAY, 
                       (screen_x - 15, screen_y - 25, health_width, 5))
        pygame.draw.rect(self.screen, self.GREEN, 
                       (screen_x - 15, screen_y - 25, int(health_width * health_ratio), 5))
        
        # Draw UI
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw UI elements."""
        state = self.sim.get_state()
        player = self.sim.player
        
        # Background for UI
        ui_bg = pygame.Surface((250, 150), pygame.SRCALPHA)
        ui_bg.fill((0, 0, 0, 180))
        self.screen.blit(ui_bg, (10, 10))
        
        # Player stats
        y_offset = 15
        
        text = self.font.render(f"Player Stats", True, self.WHITE)
        self.screen.blit(text, (15, y_offset))
        y_offset += 25
        
        text = self.small_font.render(f"Health: {int(player.health)}/{int(player.max_health)}", True, self.WHITE)
        self.screen.blit(text, (20, y_offset))
        y_offset += 20
        
        text = self.small_font.render(f"Agility: {player.agility:.1f}", True, self.WHITE)
        self.screen.blit(text, (20, y_offset))
        y_offset += 20
        
        text = self.small_font.render(f"Speed: {player.get_move_speed():.2f}", True, self.WHITE)
        self.screen.blit(text, (20, y_offset))
        y_offset += 20
        
        # Zombie count
        alive_zombies = len([z for z in self.sim.zombies if z.is_alive()])
        text = self.small_font.render(f"Zombies: {alive_zombies}", True, self.WHITE)
        self.screen.blit(text, (20, y_offset))
        y_offset += 20
        
        # Controls
        text = self.small_font.render("WASD/Arrows: Move", True, self.GRAY)
        self.screen.blit(text, (20, y_offset))
        y_offset += 18
        
        text = self.small_font.render("ESC: Quit", True, self.GRAY)
        self.screen.blit(text, (20, y_offset))
        
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    game = ZombieGame()
    game.run()


if __name__ == "__main__":
    main()
