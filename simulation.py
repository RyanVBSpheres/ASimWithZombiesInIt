"""
Zombie simulation demonstrating sound/smell mechanics and character stats.
"""
from character import Character
from trail_system import TrailSystem


class ZombieSimulation:
    """Main simulation class for zombie survival game."""
    
    def __init__(self):
        """Initialize the simulation."""
        # Create player and zombies
        self.player = Character("Player", health=100, agility=12, strength=15, x=0, y=0)
        self.zombies = [
            Character("Zombie1", health=80, agility=8, strength=10, x=10, y=10),
            Character("Zombie2", health=80, agility=8, strength=10, x=-10, y=10),
        ]
        
        # Trail system for tracking player
        self.trail_system = TrailSystem()
        
        # Simulation state
        self.tick = 0
        
    def update(self):
        """Update the simulation by one tick."""
        self.tick += 1
        
        # Update player trails
        self.trail_system.update(self.player)
        
        # Move zombies toward player trails
        for zombie in self.zombies:
            if zombie.is_alive():
                self._update_zombie(zombie)
        
        # Reset player movement state after update
        self.player.is_moving = False
    
    def _update_zombie(self, zombie):
        """
        Update a zombie using predator mechanics.
        Zombies primarily track by smell, secondarily by sound.
        
        Args:
            zombie: Zombie character to update
        """
        # Get direction to strongest trail
        dx, dy = self.trail_system.get_strongest_trail_direction(
            zombie.x, zombie.y, use_smell=True, use_sound=True
        )
        
        # Move zombie toward trail
        if dx != 0 or dy != 0:
            zombie.move(dx, dy)
        
    def move_player(self, dx, dy):
        """
        Move the player.
        
        Args:
            dx: Direction in x (-1, 0, or 1)
            dy: Direction in y (-1, 0, or 1)
        """
        self.player.move(dx, dy)
    
    def attack(self, attacker, target):
        """
        Perform an attack.
        
        Args:
            attacker: Character performing the attack
            target: Character being attacked
        """
        damage = attacker.get_attack_damage()
        target.take_damage(damage)
    
    def get_state(self):
        """Get current simulation state for display."""
        return {
            'tick': self.tick,
            'player': self.player,
            'zombies': [z for z in self.zombies if z.is_alive()],
            'trails': self.trail_system.get_trail_count(),
            'player_sound': self.trail_system.get_sound_intensity_at(
                self.player.x, self.player.y
            ),
            'player_smell': self.trail_system.get_smell_intensity_at(
                self.player.x, self.player.y
            ),
        }
    
    def print_state(self):
        """Print current simulation state."""
        state = self.get_state()
        print(f"\n=== Tick {state['tick']} ===")
        print(f"Player: {state['player']}")
        print(f"  Move Speed: {state['player'].get_move_speed():.2f}")
        print(f"  Sound Intensity: {state['player_sound']:.2f}")
        print(f"  Smell Intensity: {state['player_smell']:.2f}")
        print(f"\nZombies:")
        for zombie in state['zombies']:
            distance = ((zombie.x - self.player.x)**2 + (zombie.y - self.player.y)**2)**0.5
            print(f"  {zombie} Distance: {distance:.1f}")
        print(f"\nActive Trails: Sound={state['trails']['sound']}, Smell={state['trails']['smell']}")


def demo():
    """Run a demonstration of the simulation."""
    sim = ZombieSimulation()
    
    print("=== Zombie Simulation Demo ===")
    print("\nDemonstrating mechanics:")
    print("1. Sound is minimal when not moving")
    print("2. Smell trails the player (persists longer than sound)")
    print("3. Agility affects move speed")
    print("4. Taking damage reduces agility and move speed")
    print("5. Strength affects damage dealt")
    
    # Initial state
    sim.print_state()
    
    # Player stands still
    print("\n--- Player standing still (minimal sound) ---")
    for _ in range(3):
        sim.update()
    sim.print_state()
    
    # Player moves
    print("\n--- Player moving (creates sound and smell trails) ---")
    for i in range(5):
        sim.move_player(1, 0)  # Move right
        sim.update()
    sim.print_state()
    
    # Player stops
    print("\n--- Player stops (sound diminishes, smell persists) ---")
    for _ in range(5):
        sim.update()
    sim.print_state()
    
    # Player gets attacked
    print("\n--- Player takes damage (agility and speed reduced) ---")
    print(f"Before attack: Health={sim.player.health}, Agility={sim.player.agility:.2f}, Speed={sim.player.get_move_speed():.2f}")
    sim.attack(sim.zombies[0], sim.player)
    print(f"After attack: Health={sim.player.health}, Agility={sim.player.agility:.2f}, Speed={sim.player.get_move_speed():.2f}")
    
    # Another attack
    sim.attack(sim.zombies[0], sim.player)
    print(f"After 2nd attack: Health={sim.player.health}, Agility={sim.player.agility:.2f}, Speed={sim.player.get_move_speed():.2f}")
    
    # Move with reduced agility
    print("\n--- Player moving with reduced agility ---")
    for i in range(3):
        sim.move_player(1, 0)
        sim.update()
    sim.print_state()
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
