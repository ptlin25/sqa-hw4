import os
import random
from locust import HttpUser, LoadTestShape, between, task


class BlogReader(HttpUser):
    host = "https://jsonplaceholder.typicode.com"
    wait_time = between(1, 3)

    def on_start(self):
        self.user_id = random.randint(1, 10)
        self.post_ids = list(range(1, 101))

    @task(40)
    def browse_all_posts(self):
        self.client.get("/posts", name="GET /posts")

    @task(30)
    def read_specific_post(self):
        post_id = random.choice(self.post_ids)
        self.client.get(f"/posts/{post_id}", name="GET /posts/{id}")

    @task(20)
    def view_post_comments(self):
        post_id = random.choice(self.post_ids)
        self.client.get(
            f"/posts/{post_id}/comments", name="GET /posts/{id}/comments"
        )

    @task(10)
    def view_user_profile(self):
        self.client.get(f"/users/{self.user_id}", name="GET /users/{id}")
    

LOAD_TEST = [
    {"duration": 10, "users": 10, "spawn_rate": 10},       # ramp up to 100 VUs
    {"duration": 50, "users": 40, "spawn_rate": 10},      # hold at peak load
    {"duration": 60, "users": 0, "spawn_rate": 10},        # ramp down
]


class StagesShape(LoadTestShape):
    stages = LOAD_TEST

    def tick(self):
        t = self.get_run_time()
        for stage in self.stages:
            if t <= stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None
