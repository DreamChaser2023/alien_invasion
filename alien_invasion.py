import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        # 全屏模式
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width=self.screen.get_rect().width
        # self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
        self._make_difficulty_buttons()
        self.game_active = False


    def _make_difficulty_buttons(self):
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")

        self.easy_button.rect.top = (self.medium_button.rect.top + 1.5 * self.play_button.rect.height)
        self.easy_button._update_msg_position()
        self.medium_button.rect.top = (self.easy_button.rect.top + 1.5 * self.easy_button.rect.height)
        self.medium_button._update_msg_position()
        self.hard_button.rect.top = (self.medium_button.rect.top + 1.5 * self.medium_button.rect.height)
        self.hard_button._update_msg_position()

        self.medium_button.set_highlighted_color()

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)  # 每秒60帧

    def _check_events(self):
        # 响应鼠标和按键事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _check_keydown_events(self, event):
        # 响应按下
        # print(event.key)
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif (event.key == pygame.K_p) and (not self.game_active):
            self._start_game()

    def _check_keyup_events(self, event):
        # 响应释放
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # 创建一颗子弹，并将其加入编组 bullets
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        # print(len(self.bullets)) #查看子弹数量，验证子弹是否删除了

    def _check_bullet_alien_collisions(self):
        # 检查是否有子弹击中了外星人，如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            # 删除现有的子弹并创建一个新的外星舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_screen(self):
        # 更新屏幕上的图像，并切换到新屏幕
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitime()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
        pygame.display.flip()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                # while current_x < self.settings.screen_width :
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print(f"Ship hit!!! life remain:{self.stats.ships_left}")

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            self.sb.prep_score()
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if easy_button_clicked:
            self.settings.difficulty_level = "easy"
            self.easy_button.set_highlighted_color()
            self.medium_button.set_base_color()
            self.hard_button.set_base_color()
        elif medium_button_clicked:
            self.settings.difficulty_level = "medium"
            self.easy_button.set_base_color()
            self.medium_button.set_highlighted_color()
            self.hard_button.set_base_color()
        elif hard_button_clicked:
            self.settings.difficulty_level = "hard"
            self.easy_button.set_base_color()
            self.medium_button.set_base_color()
            self.hard_button.set_highlighted_color()

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.game_active = True
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
