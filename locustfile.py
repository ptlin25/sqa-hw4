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
    {"duration": 60, "users": 100, "spawn_rate": 10},       # ramp up to 100 VUs
    {"duration": 240, "users": 100, "spawn_rate": 10},      # hold at peak load
    {"duration": 300, "users": 0, "spawn_rate": 10},        # ramp down
]

SPIKE_TEST = [
    {"duration": 60, "users": 100, "spawn_rate": 10},       # baseline
    {"duration": 70, "users": 1000, "spawn_rate": 200},     # spike
    {"duration": 120, "users": 1000, "spawn_rate": 200},    # hold spike briefly
    {"duration": 130, "users": 100, "spawn_rate": 200},     # back to baseline
    {"duration": 240, "users": 100, "spawn_rate": 10},      # observe recovery
    {"duration": 300, "users": 0, "spawn_rate": 10},
]


class StagesShape(LoadTestShape):
    stages = LOAD_TEST

    def tick(self):
        t = self.get_run_time()
        for stage in self.stages:
            if t <= stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None
