class Settings:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # self.bg_color = ("gray")
        self.ship_limit = 0 #如果剩0，则只能死一次
        self.bullet_width = 3
        self.bullet_width = 1200 # 测试全部消灭用
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.5
        self.difficulty_level = "medium"
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        if self.difficulty_level =="easy":
            self.ship_limit = 5
            self.bullets_allowed = 10
            self.ship_speed = 0.75
            self.bullet_speed = 1.5
            self.alien_speed = 1.0
        elif self.difficulty_level =="medium":
            self.ship_limit = 3
            self.bullets_allowed = 5
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.alien_speed = 1.0
        elif self.difficulty_level =="hard":
            self.ship_limit = 1
            self.bullets_allowed = 3
            self.ship_speed = 3.0
            self.bullet_speed = 6.0
            self.alien_speed = 2.0

        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
