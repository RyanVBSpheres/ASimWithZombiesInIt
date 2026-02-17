"""
Trail system for sound and smell mechanics.
Sound and smell trail the player with smell persisting longer than sound.
"""
import math

class Trail:
    """Represents a single trail point (sound or smell)."""
    
    def __init__(self, x, y, intensity, decay_rate):
        """
        Initialize a trail point.
        
        Args:
            x: X position
            y: Y position
            intensity: Initial intensity
            decay_rate: How fast this trail point decays per tick
        """
        self.x = x
        self.y = y
        self.intensity = intensity
        self.decay_rate = decay_rate
        
    def decay(self):
        """Decay the trail intensity over time."""
        self.intensity = max(0, self.intensity - self.decay_rate)
        
    def is_active(self):
        """Check if trail is still active."""
        return self.intensity > 0
    
    def distance_to(self, x, y):
        """Calculate distance to a position."""
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


class TrailSystem:
    """Manages sound and smell trails that follow the player."""
    
    def __init__(self):
        """Initialize the trail system."""
        self.sound_trails = []
        self.smell_trails = []
        
        # Sound decays faster than smell
        self.sound_decay_rate = 0.5
        self.smell_decay_rate = 0.1  # Smell persists longer
        
        # Movement threshold for sound generation
        self.sound_movement_threshold = 0.1
        
    def add_sound(self, character):
        """
        Add a sound trail based on character movement.
        Sound is almost non-existent when not moving.
        
        Args:
            character: Character creating the sound
        """
        if character.is_moving:
            # Sound intensity based on movement speed
            move_speed = character.get_move_speed()
            if move_speed > self.sound_movement_threshold:
                # Higher speed = louder sound
                intensity = move_speed * 2.0
                self.sound_trails.append(
                    Trail(character.x, character.y, intensity, self.sound_decay_rate)
                )
        else:
            # Very minimal sound when stationary (breathing, etc.)
            intensity = 0.05  # Almost non-existent
            self.sound_trails.append(
                Trail(character.x, character.y, intensity, self.sound_decay_rate)
            )
    
    def add_smell(self, character):
        """
        Add a smell trail for the character.
        Smell always persists and trails more than sound.
        
        Args:
            character: Character creating the smell
        """
        # Smell is constant regardless of movement
        intensity = 1.0
        self.smell_trails.append(
            Trail(character.x, character.y, intensity, self.smell_decay_rate)
        )
    
    def update(self, character):
        """
        Update trails with new character position.
        
        Args:
            character: Character to track
        """
        self.add_sound(character)
        self.add_smell(character)
        
        # Decay and remove inactive trails
        self._decay_trails()
    
    def _decay_trails(self):
        """Decay all trails and remove inactive ones."""
        for trail in self.sound_trails:
            trail.decay()
        for trail in self.smell_trails:
            trail.decay()
            
        self.sound_trails = [t for t in self.sound_trails if t.is_active()]
        self.smell_trails = [t for t in self.smell_trails if t.is_active()]
    
    def get_sound_intensity_at(self, x, y, max_distance=10):
        """
        Get total sound intensity at a position.
        Predators use this to detect prey.
        
        Args:
            x: X position
            y: Y position
            max_distance: Maximum distance to consider trails
            
        Returns:
            Total sound intensity at position
        """
        total = 0
        for trail in self.sound_trails:
            distance = trail.distance_to(x, y)
            if distance < max_distance:
                # Intensity falls off with distance
                falloff = max(0, 1 - (distance / max_distance))
                total += trail.intensity * falloff
        return total
    
    def get_smell_intensity_at(self, x, y, max_distance=20):
        """
        Get total smell intensity at a position.
        Predators use this to detect prey, smell has longer range than sound.
        
        Args:
            x: X position
            y: Y position
            max_distance: Maximum distance to consider trails
            
        Returns:
            Total smell intensity at position
        """
        total = 0
        for trail in self.smell_trails:
            distance = trail.distance_to(x, y)
            if distance < max_distance:
                # Intensity falls off with distance
                falloff = max(0, 1 - (distance / max_distance))
                total += trail.intensity * falloff
        return total
    
    def get_strongest_trail_direction(self, x, y, use_smell=True, use_sound=True):
        """
        Get direction to strongest trail for predator tracking.
        Predators follow smell primarily, with sound as secondary.
        
        Args:
            x: Predator x position
            y: Predator y position
            use_smell: Whether to consider smell
            use_sound: Whether to consider sound
            
        Returns:
            Tuple of (dx, dy) normalized direction, or (0, 0) if no trails
        """
        best_x, best_y = 0, 0
        max_intensity = 0
        
        # Check smell trails first (primary tracking method)
        if use_smell:
            for trail in self.smell_trails:
                distance = trail.distance_to(x, y)
                if distance > 0 and distance < 20:
                    falloff = max(0, 1 - (distance / 20))
                    intensity = trail.intensity * falloff * 2.0  # Smell weighted higher
                    if intensity > max_intensity:
                        max_intensity = intensity
                        best_x, best_y = trail.x, trail.y
        
        # Check sound trails (secondary tracking method)
        if use_sound:
            for trail in self.sound_trails:
                distance = trail.distance_to(x, y)
                if distance > 0 and distance < 10:
                    falloff = max(0, 1 - (distance / 10))
                    intensity = trail.intensity * falloff
                    if intensity > max_intensity:
                        max_intensity = intensity
                        best_x, best_y = trail.x, trail.y
        
        if max_intensity > 0:
            # Return normalized direction
            dx = best_x - x
            dy = best_y - y
            magnitude = math.sqrt(dx * dx + dy * dy)
            if magnitude > 0:
                return (dx / magnitude, dy / magnitude)
        
        return (0, 0)
    
    def get_trail_count(self):
        """Get current trail counts for debugging."""
        return {
            'sound': len(self.sound_trails),
            'smell': len(self.smell_trails)
        }
