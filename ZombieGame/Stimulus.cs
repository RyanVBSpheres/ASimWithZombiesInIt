using Microsoft.Xna.Framework;
using System;

namespace ZombieGame;

/// <summary>
/// Represents a stimulus (sound or smell) that can attract zombies
/// </summary>
public class Stimulus
{
    public Vector2 Position { get; set; }
    public float Intensity { get; set; }
    public StimulusType Type { get; set; }
    public float Duration { get; set; }
    public float MaxRange { get; set; }

    public Stimulus(Vector2 position, float intensity, StimulusType type, float duration = 5f)
    {
        Position = position;
        Intensity = intensity;
        Type = type;
        Duration = duration;
        MaxRange = intensity * 100f; // Range proportional to intensity
    }

    public void Update(float deltaTime)
    {
        Duration -= deltaTime;
        // Sounds decay faster than smells - using frame-rate independent decay
        if (Type == StimulusType.Sound)
        {
            Intensity *= MathF.Pow(0.95f, deltaTime * 60f);
        }
        else
        {
            Intensity *= MathF.Pow(0.98f, deltaTime * 60f);
        }
    }

    public bool IsExpired => Duration <= 0 || Intensity < 0.01f;

    public float GetIntensityAt(Vector2 position)
    {
        float distance = Vector2.Distance(Position, position);
        if (distance > MaxRange) return 0f;
        
        // Intensity falls off with distance
        float falloff = 1f - (distance / MaxRange);
        return Intensity * falloff;
    }
}

public enum StimulusType
{
    Sound,
    Smell
}
