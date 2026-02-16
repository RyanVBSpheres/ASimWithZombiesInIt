#!/usr/bin/env python3
"""
Demo script to showcase circular detection vs square detection.

This script demonstrates why circular detection is superior to square detection
by showing how entities at the same Manhattan/Chebyshev distance can be at 
different Euclidean distances.
"""

from simulation import distance, Player, Zombie
import math

def demo_circular_vs_square():
    """Demonstrate circular vs square detection."""
    
    print("=" * 70)
    print("CIRCULAR DETECTION vs SQUARE DETECTION DEMONSTRATION")
    print("=" * 70)
    
    zombie = Zombie(100, 100)
    player = Player(100, 100)
    
    print(f"\nZombie position: ({zombie.x}, {zombie.y})")
    print(f"Player sound range: {player.sound_range}")
    print(f"Player smell range: {player.smell_range}")
    
    # Test various positions
    test_positions = [
        # (x, y, description)
        (100 + 50, 100, "50 units East"),
        (100, 100 + 50, "50 units South"),
        (100 + 35, 100 + 35, "35 units SE (diagonal)"),
        (100 + 50, 100 + 50, "50 units SE (diagonal)"),
        (100 + 75, 100, "75 units East"),
        (100 + 53, 100 + 53, "53 units SE (diagonal)"),
    ]
    
    print("\n" + "-" * 70)
    print("Testing different player positions:")
    print("-" * 70)
    
    for x, y, desc in test_positions:
        player.x = x
        player.y = y
        
        # Calculate distances
        euclidean = distance(zombie.get_pos(), player.get_pos())
        manhattan = abs(x - zombie.x) + abs(y - zombie.y)
        chebyshev = max(abs(x - zombie.x), abs(y - zombie.y))
        
        # Check detection
        zombie.find_target(player, [])
        detected = zombie.target is not None
        
        print(f"\nPlayer at {desc}:")
        print(f"  Position: ({x}, {y})")
        print(f"  Euclidean (circular) distance: {euclidean:.1f}")
        print(f"  Manhattan (diamond) distance:  {manhattan:.1f}")
        print(f"  Chebyshev (square) distance:   {chebyshev:.1f}")
        print(f"  Within smell range (100)? {euclidean <= player.smell_range}")
        print(f"  Detected by zombie? {detected}")
        
        # Show why this matters
        if detected:
            if euclidean > player.smell_range:
                print(f"  → Detected via SOUND range (not smell)")
            else:
                print(f"  → Detected via smell range")
        else:
            if chebyshev <= player.smell_range:
                print(f"  → Would be detected with SQUARE detection!")
                print(f"  → Circular detection is more realistic!")
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT:")
    print("=" * 70)
    print("• Circular (Euclidean) distance: sqrt(dx² + dy²)")
    print("  - More realistic (sound/smell spreads in all directions equally)")
    print("  - Diagonal distances are longer than cardinal directions")
    print()
    print("• Square (Chebyshev) distance: max(|dx|, |dy|)")
    print("  - Less realistic (treats diagonal same as cardinal)")
    print("  - Creates square detection zones")
    print()
    print("• Diamond (Manhattan) distance: |dx| + |dy|)")
    print("  - Also unrealistic (penalizes diagonal movement)")
    print("  - Creates diamond detection zones")
    print("=" * 70)

def demo_circle_geometry():
    """Show the mathematical difference between circle and square."""
    
    print("\n" + "=" * 70)
    print("CIRCLE vs SQUARE GEOMETRY")
    print("=" * 70)
    
    radius = 100
    
    # Points on circle vs square
    print(f"\nFor a radius/side of {radius}:")
    print()
    
    # Cardinal directions (same for both)
    print("Cardinal directions (N, S, E, W):")
    print(f"  Distance from center: {radius}")
    print(f"  Same for both circle and square ✓")
    
    # Diagonal directions (different!)
    diagonal_circle = radius
    diagonal_square = radius * math.sqrt(2)
    
    print(f"\nDiagonal directions (NE, SE, SW, NW):")
    print(f"  Circle: distance from center = {diagonal_circle:.1f}")
    print(f"  Square: distance from center = {diagonal_square:.1f}")
    print(f"  Difference: {diagonal_square - diagonal_circle:.1f} units!")
    print(f"  Square corners are {(diagonal_square/diagonal_circle - 1) * 100:.1f}% farther")
    
    print("\n" + "-" * 70)
    print("This means with SQUARE detection:")
    print("  • Zombies could detect you from farther away on diagonals")
    print("  • OR miss you when you're the same 'range' away on diagonals")
    print("  • Creates unfair gameplay and unrealistic behavior")
    print()
    print("With CIRCULAR detection (our implementation):")
    print("  • All points at the same distance are treated equally")
    print("  • Realistic sound/smell propagation")
    print("  • Fair and consistent gameplay")
    print("=" * 70)

if __name__ == "__main__":
    demo_circular_vs_square()
    demo_circle_geometry()
    
    print("\n✓ Run 'python simulation.py' to see it in action!")
