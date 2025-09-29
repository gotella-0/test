# Upgraded Catch Game

An enhanced version of a classic catch-the-falling-objects game built with Python and Pygame. This upgraded version includes multiple object types, particle effects, progressive difficulty, and polished visuals.

## Features

- **Multiple Object Types**:
  - Red Circles: Normal objects worth 1 point
  - Green Diamonds: Bonus objects worth 5 points
  - Yellow Ovals: Extra life objects
  - Purple Squares: Bombs that cost you a life

- **Progressive Difficulty**:
  - Level system that increases as you score more points
  - Falling objects spawn faster at higher levels
  - Challenge increases as you progress

- **Visual Enhancements**:
  - Particle effects for object collection and explosions
  - Distinct shapes and colors for different object types
  - Polished player character design
  - Clean UI with score, level, and lives display

- **Game States**:
  - Start screen with instructions
  - Active gameplay
  - Game over screen with final score
  - Restart functionality

## Requirements

- Python 3.6 or higher
- Pygame library

## Installation

1. Ensure you have Python installed on your system
2. Install Pygame using pip:
   ```
   pip install pygame
   ```

## How to Play

1. Run the game:
   ```
   python game.py
   ```

2. From the start screen, press SPACE to begin

3. Controls:
   - Left Arrow Key: Move player left
   - Right Arrow Key: Move player right

4. Game Objective:
   - Catch falling objects to earn points
   - Avoid bombs (purple squares)
   - Collect extra life objects (yellow ovals) to increase lives
   - Progress through levels by scoring points

5. Game Elements:
   - Red Circle: +1 point
   - Green Diamond: +5 points
   - Yellow Oval: +1 life (up to maximum of 5)
   - Purple Square: Lose 1 life

6. Game Over:
   - Game ends when all lives are lost
   - Press R to restart after game over

## Game Mechanics

- You start with 3 lives
- Missing objects (except bombs) costs 1 life
- Collecting bombs costs 1 life
- Collecting extra life objects gives you 1 additional life (maximum 5)
- Level increases every 10 points scored
- Object spawn rate increases with each level

## Code Structure

The game is organized into several classes:

- `Particle`: Handles visual effects
- `Player`: Manages player movement and rendering
- `FallingObject`: Represents the various falling objects
- `Game`: Main game controller handling states, events, and updates

## Possible Enhancements

Ideas for further improving the game:

1. Add background music and sound effects
2. Implement high score saving/loading
3. Add more power-up types
4. Create different themes or visual styles
5. Add multiplayer support
6. Implement different game modes (timed mode, survival mode, etc.)

## License

This project is open source and available under the MIT License.
