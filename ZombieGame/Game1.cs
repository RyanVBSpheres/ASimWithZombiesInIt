using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using System;
using System.Collections.Generic;
using System.Linq;

namespace ZombieGame;

public class Game1 : Game
{
    private GraphicsDeviceManager _graphics;
    private SpriteBatch _spriteBatch;
    private Texture2D _pixel;
    
    private Player _player;
    private List<Zombie> _zombies;
    private List<Stimulus> _stimuli;
    private World _world;
    private Random _random;
    
    private const int ScreenWidth = 1280;
    private const int ScreenHeight = 720;

    public Game1()
    {
        _graphics = new GraphicsDeviceManager(this);
        Content.RootDirectory = "Content";
        IsMouseVisible = true;
        
        _graphics.PreferredBackBufferWidth = ScreenWidth;
        _graphics.PreferredBackBufferHeight = ScreenHeight;
    }

    protected override void Initialize()
    {
        _random = new Random();
        _stimuli = new List<Stimulus>();
        
        // Initialize player at center
        _player = new Player(new Vector2(ScreenWidth / 2, ScreenHeight / 2));
        
        // Create zombies scattered around the map
        _zombies = new List<Zombie>();
        for (int i = 0; i < 20; i++)
        {
            Vector2 position = new Vector2(
                _random.Next(50, ScreenWidth - 50),
                _random.Next(50, ScreenHeight - 50)
            );
            _zombies.Add(new Zombie(position, _random));
        }
        
        // Generate world
        _world = new World(ScreenWidth, ScreenHeight, _random);

        base.Initialize();
    }

    protected override void LoadContent()
    {
        _spriteBatch = new SpriteBatch(GraphicsDevice);

        // Create a 1x1 white pixel texture for drawing shapes
        _pixel = new Texture2D(GraphicsDevice, 1, 1);
        _pixel.SetData(new[] { Color.White });
    }

    protected override void Update(GameTime gameTime)
    {
        if (GamePad.GetState(PlayerIndex.One).Buttons.Back == ButtonState.Pressed || Keyboard.GetState().IsKeyDown(Keys.Escape))
            Exit();

        float deltaTime = (float)gameTime.ElapsedGameTime.TotalSeconds;
        
        // Update player and collect new stimuli
        var newStimuli = _player.Update(deltaTime, ScreenWidth, ScreenHeight);
        _stimuli.AddRange(newStimuli);
        
        // Update all stimuli
        foreach (var stimulus in _stimuli)
        {
            stimulus.Update(deltaTime);
        }
        
        // Remove expired stimuli
        _stimuli.RemoveAll(s => s.IsExpired);
        
        // Update all zombies
        foreach (var zombie in _zombies)
        {
            zombie.Update(deltaTime, _stimuli);
            
            // Keep zombies in bounds
            zombie.Position = new Vector2(
                MathHelper.Clamp(zombie.Position.X, zombie.Size/2, ScreenWidth - zombie.Size/2),
                MathHelper.Clamp(zombie.Position.Y, zombie.Size/2, ScreenHeight - zombie.Size/2)
            );
        }

        base.Update(gameTime);
    }

    protected override void Draw(GameTime gameTime)
    {
        GraphicsDevice.Clear(new Color(40, 40, 30)); // Dark ground color

        _spriteBatch.Begin();
        
        // Draw world objects
        _world.Draw(_spriteBatch, _pixel);
        
        // Draw stimuli (for debugging - optional visual feedback)
        foreach (var stimulus in _stimuli)
        {
            Color stimulusColor = stimulus.Type == StimulusType.Sound 
                ? new Color(255, 255, 0, 50) // Yellow for sound
                : new Color(0, 255, 0, 30);  // Green for smell
            
            int radius = (int)(stimulus.Intensity * 50);
            Rectangle rect = new Rectangle(
                (int)(stimulus.Position.X - radius),
                (int)(stimulus.Position.Y - radius),
                radius * 2,
                radius * 2
            );
            _spriteBatch.Draw(_pixel, rect, stimulusColor);
        }
        
        // Draw zombies
        foreach (var zombie in _zombies)
        {
            zombie.Draw(_spriteBatch, _pixel);
        }
        
        // Draw player on top
        _player.Draw(_spriteBatch, _pixel);
        
        _spriteBatch.End();

        base.Draw(gameTime);
    }
}
