import json
import os

class ScoreSystem:
    def __init__(self):
        self.score = 0
        self.time_elapsed = 0
        self.leaderboard_path = os.path.join(
            os.path.dirname(__file__), '../../data/leaderboard.json'
        )

    def update(self, dt):
        self.time_elapsed += dt
        if self.time_elapsed >= 1000:
            self.score += 1
            self.time_elapsed = 0

    def add_dodge_bonus(self):
        self.score += 10

    def draw(self, screen, font):
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

    def save_to_leaderboard(self):
        """Append current score to leaderboard.json, sorted descending."""
        path = self.leaderboard_path

        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = []
        else:
            scores = []

        scores.append({"score": self.score})
        scores.sort(key=lambda x: x["score"], reverse=True)

        with open(path, 'w') as f:
            json.dump(scores, f, indent=2)