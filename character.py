"""
Character class for the zombie simulation.
Handles base stats like health, agility, and strength.
"""

class Character:
    """Base character class with health, agility, and strength stats."""
    
    def __init__(self, name, health=100, agility=10, strength=10, x=0, y=0):
        """
        Initialize a character.
        
        Args:
            name: Character name
            health: Initial health (0-100)
            agility: Agility stat (determines move speed)
            strength: Strength stat (determines damage)
            x: Initial x position
            y: Initial y position
        """
        self.name = name
        self.max_health = health
        self.health = health
        self.base_agility = agility
        self.agility = agility
        self.strength = strength
        self.x = x
        self.y = y
        self.is_moving = False
        
    def get_move_speed(self):
        """Calculate move speed based on current agility."""
        return self.agility / 10.0
    
    def update_agility_from_health(self):
        """Update agility based on current health percentage."""
        health_percentage = self.health / self.max_health
        self.agility = self.base_agility * health_percentage
        
    def take_damage(self, damage):
        """
        Take damage and update agility accordingly.
        
        Args:
            damage: Amount of damage to take
        """
        self.health = max(0, self.health - damage)
        self.update_agility_from_health()
        
    def move(self, dx, dy):
        """
        Move the character by the given deltas.
        
        Args:
            dx: Change in x position
            dy: Change in y position
        """
        move_speed = self.get_move_speed()
        self.x += dx * move_speed
        self.y += dy * move_speed
        self.is_moving = (dx != 0 or dy != 0)
        
    def get_attack_damage(self):
        """Get the damage this character deals in an attack."""
        return self.strength
    
    def is_alive(self):
        """Check if character is still alive."""
        return self.health > 0
    
    def __repr__(self):
        return f"{self.name}(HP:{self.health:.1f}, Agi:{self.agility:.1f}, Str:{self.strength}, Pos:({self.x:.1f},{self.y:.1f}))"
