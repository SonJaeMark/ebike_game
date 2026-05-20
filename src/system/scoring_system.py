class ScoreSystem:
    def __init__(self):
        self.score = 0
        self.time_elapsed = 0

    def update(self, dt):
        # Add 1 point every second survived
        self.time_elapsed += dt
        if self.time_elapsed >= 1000:  # 1000ms = 1 second
            self.score += 1
            self.time_elapsed = 0

    def add_dodge_bonus(self):
        self.score += 10

    def draw(self, screen, font):
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))