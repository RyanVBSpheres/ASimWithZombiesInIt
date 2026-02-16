# ASimWithZombiesInIt
Top Down Zombie Survival Sim

## Description
A top-down 2D C# MonoGame where you must survive in a zombie-infested apocalypse world. Zombies use simple AI to be attracted to sounds and smells - louder sounds and stronger smells pull them more effectively. The player must carefully manage their movement to avoid attracting the undead.

## Features
- **Player Controls**: WASD to move around the world
- **Zombie AI**: Zombies are attracted to sounds and smells with realistic intensity falloff
  - Sounds (footsteps) attract zombies more immediately but decay faster
  - Smells (player scent) have longer duration but weaker attraction
  - Zombies wander when no stimuli are detected
- **Environmental Objects**: The world contains various apocalypse scenario elements:
  - Trees and rocks (nature)
  - Ruined buildings
  - Abandoned cars
- **Stimulus System**: Visual feedback shows sound (yellow) and smell (green) propagation

## How to Run
```bash
cd ZombieGame
dotnet run
```

## Requirements
- .NET 9.0 or higher
- MonoGame Framework 3.8+

## Controls
- **W**: Move up
- **A**: Move left  
- **S**: Move down
- **D**: Move right
- **Escape**: Exit game

## Gameplay Tips
- Moving creates footstep sounds that attract zombies
- Standing still reduces sound but you still emit smell
- Watch the visual stimulus indicators to see your detection range
- Zombies shown in dark green, player in blue

