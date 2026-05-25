# E-Bike Game

## What is this game?

`E-Bike Game` is a Python arcade-style driving game built with `pygame`. The player controls an electric bike and moves across a 4-lane road to dodge incoming obstacles.

Gameplay features:
- Start screen, pause screen, leaderboard, and game over state
- Player name input and score persistence in `data/leaderboard.json`
- Three difficulty levels based on score
- Video background using OpenCV for animated environment rendering
- Sound effects for movement, collisions, and game music

## How to set up

1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Run the game:

```powershell
python src/main.py
```

> Make sure the `src/assets/` folder and `data/leaderboard.json` file are present, as the game loads images, sound files, and video assets at runtime.

## Dependencies and libraries used

The game depends on the following Python packages:

- `pygame` – main game engine for rendering, input, audio, and game loop
- `numpy` – used to transform video frames before rendering them in `pygame`
- `opencv-python` – loads and reads the video assets used for the game background and game-over screen
- `pytmx` – included in `requirements.txt`; not currently referenced in the main game source

The code also uses Python standard libraries:
- `sys`, `os`, `json`, `random`, `enum`

## Project structure

- `src/main.py` – entry point and main game loop
- `src/core/settings.py` – game configuration, screen size, lane definitions, and gameplay constants
- `src/entities/ebike.py` – player bike movement, lane logic, drawing, and collision detection
- `src/entities/obstacles/obstacles.py` – obstacle spawning, movement, scaling, and rendering
- `src/entities/obstacles/obs.py` – obstacle type enumeration
- `src/scenes/game_scene.py` – scene rendering and state-specific layouts such as menu, pause, leaderboard, and game over
- `src/system/audio_system.py` – sound and music playback functions
- `src/system/scoring_system.py` – score tracking and leaderboard persistence
- `data/leaderboard.json` – saved high score list

## Key game methods and classes

### `src/main.py`

- Initializes `pygame`, audio, screen, and resources
- Manages the main game state machine: `MENU`, `NAME_INPUT`, `PLAY`, `PAUSE`, `LEADERBOARD`, and `GAME_OVER`
- Handles input for navigation, pausing, name entry, and quitting
- Controls difficulty progression, obstacle count, and life management
- Uses `in_game_scene()` to render gameplay and return collision events

### `src/entities/ebike.py`

- `Ebike.__init__()` – sets up bike position, lane geometry, and loads the bike sprite
- `handle_input(play_move_sound)` – reads keyboard input and updates target lane or vertical position
- `update_lane()` – smoothly animates the bike between lanes
- `snap_to_perspective_lane()` – converts lane position into a screen coordinate using perspective interpolation
- `update()` – updates the bike position each frame
- `draw(screen)` – draws the bike sprite
- `is_colliding(obstacle_obj)` – checks collision against obstacle bounding boxes

### `src/entities/obstacles/obstacles.py`

- `Obstacles.__init__()` – creates obstacle state with type, image, and motion vector
- `reset()` – chooses a random obstacle type and reinitializes it
- `pick_lane_and_initialize()` – selects a lane and sets obstacle movement direction
- `load_image()` – loads the appropriate obstacle sprite based on type
- `scale_obstacle()` – scales the obstacle sprite dynamically to preserve perspective as it moves
- `update()` – advances obstacle position and resets it when it passes beyond screen bottom
- `draw(screen)` – updates obstacle and blits it to the screen
- `rect` property – returns the obstacle hitbox used for collision detection

### `src/scenes/game_scene.py`

- `in_game_scene(...)` – renders the background, road lines, obstacles, player, and collision handling
- `pause_menu(screen, font, WIDTH, HEIGHT, pause_image)` – draws the pause screen
- `game_over(screen, font, score_system, WIDTH, HEIGHT, player_name, game_over_video)` – displays game over video and final score
- `game_menu(screen, font, WIDTH, HEIGHT, menu_image)` – shows the main menu image
- `leaderboard(screen, font, WIDTH, HEIGHT, leaderboard_image)` – reads `data/leaderboard.json` and renders top scores
- `get_player_name(screen, font, WIDTH, HEIGHT, menu_image, player_name)` – displays text input for player name

### `src/system/audio_system.py`

- `init_audio()` – initializes `pygame.mixer`
- `play_move_sound()` – plays the bike movement sound
- `play_dog_hit_sound()`, `play_cat_hit_sound()`, `play_bato_hit_sound()` – play obstacle collision sounds
- `play_game_over_music()` – begins looped game over music
- `stop_game_over_music()` – stops music playback
- `play_in_game_music()` / `restart_in_game_music()` – manage in-game background music

### `src/system/scoring_system.py`

- `ScoreSystem.__init__()` – initializes score tracking and leaderboard file path
- `update(dt)` – increases score over time
- `add_dodge_bonus()` – awards extra points when obstacles pass safely
- `draw(screen, font)` – renders the current score on screen
- `save_to_leaderboard(player_name)` – saves the score and player name to JSON leaderboard

## Controls

- Arrow keys or `A` / `D`: move left / right lanes
- Arrow keys or `W` / `S`: move forward / backward on the same lane
- `SPACE`: pause / resume while playing
- `ENTER`: start game or confirm name input
- `L`: open leaderboard from the main menu
- `ESC`: back or quit

## Notes

- The game uses a 4-lane perspective road and simulates depth by scaling obstacles as they move downward.
- Score is stored in `data/leaderboard.json`, and the top ten entries are shown in the leaderboard screen.
- The `requirements.txt` file includes `pytmx` even though the current source code does not import it.
