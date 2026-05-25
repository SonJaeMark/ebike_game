# Project Details

## Libraries used

### `pygame`
The game is built primarily with `pygame`, which provides window creation, input handling, image rendering, audio playback, fonts, and collision helpers.

Pygame APIs used in this project:
- `pygame.init()` – initializes all imported pygame modules
- `pygame.display.set_mode((WIDTH, HEIGHT))` – creates the game window
- `pygame.display.set_caption("E-Bike Game")` – sets the window title
- `pygame.time.Clock()` – creates the clock used to regulate FPS
- `clock.tick(FPS)` – limits the game loop to the configured frame rate
- `pygame.event.get()` – polls input events
- `pygame.QUIT` – detects window close events
- `pygame.KEYDOWN`, `pygame.K_LEFT`, `pygame.K_a`, `pygame.K_RIGHT`, `pygame.K_d`, `pygame.K_UP`, `pygame.K_w`, `pygame.K_DOWN`, `pygame.K_s`, `pygame.K_SPACE`, `pygame.K_RETURN`, `pygame.K_ESCAPE`, `pygame.K_l`, `pygame.K_BACKSPACE` – keyboard controls
- `pygame.key.get_pressed()` – checks continuous key state for smooth movement
- `pygame.Rect(...)` and `.colliderect(...)` – collision detection between player and obstacles
- `pygame.image.load(path).convert_alpha()` – loads PNG/WebP sprite assets with transparency
- `pygame.transform.scale(...)`, `pygame.transform.smoothscale(...)`, `pygame.transform.rotate(...)` – resize and rotate visual assets
- `pygame.font.SysFont('Arial', size)` – loads a font for text rendering
- `font.render(text, antialias, color)` – creates text surfaces for score, menus, and prompts
- `screen.blit(surface, position)` – draws images and text to the screen
- `pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)` – creates transparent overlay surfaces
- `pygame.mixer.init()` – initializes sound playback
- `pygame.mixer.Sound(path).play()` – plays short sound effects
- `pygame.mixer.music.load(path)`, `.set_volume()`, `.play(-1)`, `.stop()` – plays and controls background music

### `opencv-python` (`cv2`)
The game uses OpenCV to read and process video assets for the animated background and the game over screen.

OpenCV APIs used:
- `cv2.VideoCapture(path)` – opens a video file for frame-by-frame reading
- `.get(cv2.CAP_PROP_FPS)` – reads the video FPS value
- `.read()` – retrieves the next frame from the video
- `.grab()` – advances the video by one frame without decoding it
- `.set(cv2.CAP_PROP_POS_FRAMES, 0)` – rewinds the video loop
- `cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)` – converts OpenCV’s BGR frames to RGB for pygame
- `cv2.resize(frame, (WIDTH, HEIGHT))` – resizes frames to the game window dimensions

### `numpy`
Numpy is used to rearrange video frame data before converting it into a pygame surface.

Numpy APIs used:
- `np.transpose(frame, (1, 0, 2))` – swaps the x/y axes of the image before creating a pygame surface
- `.tobytes()` – converts the NumPy frame to raw bytes for `pygame.image.frombuffer`

### `pytmx`
- `pytmx` is listed in `requirements.txt` but is not directly imported or used by the current source code.

### Python standard library
- `json` – load and save leaderboard scores in `data/leaderboard.json`
- `os` – construct file paths portably and test for file existence
- `sys` – exit the game cleanly at the end of the loop
- `random` – choose random obstacle types and lanes
- `enum.Enum` – define obstacle types in `ObstaclesEnum`

## Methods from libraries that are used

### `pygame` core methods in use
- `pygame.init()`: Start pygame subsystem
- `pygame.display.set_mode()`: Create the game window
- `pygame.display.set_caption()`: Label the window
- `pygame.time.Clock()` / `.tick(FPS)`: Maintain consistent frame rate
- `pygame.event.get()`: Read events each frame
- `pygame.key.get_pressed()`: Detect held keys for movement
- `pygame.image.load()`, `.convert_alpha()`: Load sprite images and preserve transparency
- `pygame.transform.scale()`, `.smoothscale()`, `.rotate()`: Manipulate sprite sizes and orientation
- `pygame.font.SysFont()` / `.render()`: Render text labels and scores
- `pygame.Surface()`: Build overlays and custom surfaces
- `pygame.Rect()`: Create rectangles for collision detection
- `pygame.mixer.init()`, `pygame.mixer.Sound(...).play()`, `pygame.mixer.music.load()`, `.play(-1)`, `.stop()`: Audio playback

### `opencv-python` methods in use
- `cv2.VideoCapture()`: Open and read video files
- `VideoCapture.read()`: Fetch video frames
- `VideoCapture.grab()`: Advance video frames without decode
- `VideoCapture.set()`: Reset video to beginning for looping
- `cv2.cvtColor()`: Convert BGR frames to RGB color space
- `cv2.resize()`: Resize frames to fit the game window

### `numpy` methods in use
- `np.transpose()`: Adjust frame axis order for pygame conversion
- `.tobytes()`: Convert frame data to raw bytes buffer

### `json` methods in use
- `json.load()`: Read leaderboard contents from JSON file
- `json.dump()`: Write sorted leaderboard scores back to JSON

## Core functions and classes

### `src/main.py`
This is the game entrypoint and engine loop.
- `reset_full_game_state()`: Reset life, player, obstacles, score, and game state before starting a new run
- main loop: processes events, updates gameplay, routes states, draws the current scene, flips the display, and exits cleanly
- game state management: `MENU`, `NAME_INPUT`, `PLAY`, `PAUSE`, `LEADERBOARD`, `GAME_OVER`
- input handling for menu navigation, pause/resume, name entry, and quitting
- difficulty management: select level based on score and adjust obstacle count and speed
- collision handling: call `in_game_scene()` and react to hits with sound and life reduction

### `src/entities/ebike.py`
Defines player movement, lane logic, rendering, and collision detection.
- `Ebike.__init__()`: Initialize position, lane centers, sprite, and movement state
- `update_lane()`: Smoothly interpolate the bike between lane positions
- `snap_to_perspective_lane()`: Convert lane index and vertical position into a perspective-correct x coordinate
- `handle_input(play_move_sound)`: Move left/right/lane and forward/backward using keyboard input, and play movement sound once per lane change
- `update()`: Apply lane interpolation and position snapping each frame
- `draw(screen)`: Draw the player bike sprite
- `is_colliding(obstacle_obj)`: Return whether the bike collides with an obstacle rectangle

### `src/entities/obstacles/obstacles.py`
Handles obstacle lifecycle, rendering, motion, and perspective scaling.
- `Obstacles.__init__()`: Set type, initial sizes, movement speed, and call `reset()`
- `reset()`: Pick a random obstacle type, reload image, and initialize lane movement
- `pick_lane_and_initialize()`: Choose a random lane and create the movement direction towards the end-of-lane point
- `load_image()`: Load the obstacle sprite for the selected type, or create a fallback surface if missing
- `scale_obstacle()`: Scale obstacle graphics as it moves downward to simulate depth
- `update()`: Move the obstacle each frame and reset it when it passes off the bottom of the screen
- `draw(screen)`: Update and draw the obstacle
- `rect`: Expose the current hitbox rectangle for collision checks

### `src/entities/obstacles/obs.py`
- `ObstaclesEnum`: Defines obstacle types `CAT`, `DOG`, and `BATO`

### `src/scenes/game_scene.py`
Render logic for gameplay and non-play states.
- `in_game_scene(...)`: Render the video background, draw road lines and obstacles, detect collisions, and add dodge bonus points
- `pause_menu(...)`: Draw the pause screen background
- `game_over(...)`: Render the game over screen with looping video and display final score
- `game_menu(...)`: Draw the main menu background image
- `leaderboard(...)`: Read the leaderboard file, sort top scores, and render the top 10 entries
- `get_player_name(...)`: Draw the name entry screen and current typed name

### `src/system/audio_system.py`
Audio initialization and playback helpers.
- `init_audio()`: Initialize pygame mixer subsystem
- `play_move_sound()`: Play lane-change / move sound effect
- `play_dog_hit_sound()`, `play_cat_hit_sound()`, `play_bato_hit_sound()`: Play collision sounds for each obstacle type
- `play_game_over_music()`: Start looping game over music
- `stop_game_over_music()`: Stop current music playback
- `play_in_game_music()`, `restart_in_game_music()`: Start and restart in-game background music

### `src/system/scoring_system.py`
Score and leaderboard persistence.
- `ScoreSystem.__init__()`: Initialize score state and leaderboard file path
- `update(dt)`: Increase score over time based on elapsed milliseconds
- `add_dodge_bonus()`: Award points when obstacles travel past without collision
- `draw(screen, font)`: Render the current score to the screen
- `save_to_leaderboard(player_name)`: Save the score to `data/leaderboard.json` and keep the list sorted

## Notes

- The game combines `pygame` rendering with OpenCV video playback, which is unusual for a simple arcade game but allows animated video backgrounds.
- `numpy` is only used to reshape video frame data for conversion into `pygame.Surface` objects.
- `pytmx` is installed but not used; it may be a leftover dependency or intended for a future tile map feature.
