import sys
import time
import pygame
from pygame.locals import *


class StartupWindow:
    def __init__(self):
        self.size = 600
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Welcome to Virtual Pet Simulator")

        self.background_color = (219, 211, 173)
        self.play_button_image = pygame.image.load("play_button.png")
        self.play_button_rect = self.play_button_image.get_rect(center=(self.size // 2, self.size // 2))

        self.icon = pygame.image.load("icon.png")

        pygame.display.set_icon(self.icon)

        pygame.display.set_icon(pygame.image.load("windowicon.png"))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if self.play_button_rect.collidepoint(event.pos):
                        self.start_game()

            self.screen.fill(self.background_color)

            self.screen.blit(self.play_button_image, self.play_button_rect)

            pygame.display.flip()

    def start_game(self):
        pet_choice_dialog = PetChoiceDialog(self.screen, self.background_color)
        pet_type = pet_choice_dialog.run()
        if pet_type:
            pet_name_dialog = PetNameDialog(self.screen, self.background_color)
            pet_name = pet_name_dialog.run()
            if pet_name:
                game_window = MainWindow(self.screen, pet_type, pet_name, self.background_color)
                game_window.run()


class PetChoiceDialog:
    def __init__(self, screen, background_color):
        self.goldfish_button_rect = None
        self.cat_button_rect = None
        self.pug_button_rect = None
        self.size = None
        self.screen = screen
        self.background_color = background_color
        self.font = pygame.font.Font("8bitOperatorPlus8-Regular.ttf", 36)

        self.pug_button_image = pygame.image.load("pug_button.png")
        self.cat_button_image = pygame.image.load("cat_button.png")
        self.goldfish_button_image = pygame.image.load("goldfish_button.png")

        self.size = self.screen.get_width()

        self.button_width = 200
        self.button_height = 100
        self.button_left_margin = (600 - self.button_width) // 2
        self.button_top_margin = (600 - 3 * self.button_height - 2 * 50) // 2

    def run(self):
        pet_type = None
        while not pet_type:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if self.pug_button_rect.collidepoint(event.pos):
                        pet_type = "Pug"
                    elif self.cat_button_rect.collidepoint(event.pos):
                        pet_type = "Cat"
                    elif self.goldfish_button_rect.collidepoint(event.pos):
                        pet_type = "Goldfish"

            self.screen.fill(self.background_color)

            self.pug_button_rect = self.pug_button_image.get_rect(
                topleft=(self.button_left_margin, self.button_top_margin))
            self.cat_button_rect = self.cat_button_image.get_rect(
                topleft=(self.button_left_margin, self.button_top_margin + self.button_height + 50))
            self.goldfish_button_rect = self.goldfish_button_image.get_rect(
                topleft=(self.button_left_margin, self.button_top_margin + 2 * (self.button_height + 50)))

            self.screen.blit(self.pug_button_image, self.pug_button_rect)
            self.screen.blit(self.cat_button_image, self.cat_button_rect)
            self.screen.blit(self.goldfish_button_image, self.goldfish_button_rect)

            text = "Choose your First Pet!"
            outline_color = (0, 0, 0)
            shadow_color = (0, 0, 0)
            text_surface = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.size // 2, self.button_top_margin - 50))

            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    self.screen.blit(self.font.render(text, True, outline_color), (text_rect.x + dx, text_rect.y + dy))

            self.screen.blit(self.font.render(text, True, shadow_color), (text_rect.x + 2, text_rect.y + 2))

            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

        return pet_type


class PetNameDialog:
    def __init__(self, screen, background_color):
        self.size = None
        self.screen = screen
        self.background_color = background_color
        self.font = pygame.font.Font("8bitOperatorPlus8-Regular.ttf", 24)
        self.text_input_value = ""

    def run(self):
        text_input_active = True
        while text_input_active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        text_input_active = False
                    elif event.key == K_BACKSPACE:
                        self.text_input_value = self.text_input_value[:-1]
                    else:
                        self.text_input_value += event.unicode

            self.screen.fill(self.background_color)

            text_input_rect = pygame.Rect(100, 400, 400, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), text_input_rect)
            text_surface = self.font.render(self.text_input_value, True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                midleft=(text_input_rect.x + 10, text_input_rect.centery))
            self.screen.blit(text_surface, text_rect)

            instruction_text = "Choose a name for your new pet!"
            outline_color = (0, 0, 0)
            shadow_color = (0, 0, 0)
            instruction_surface = self.font.render(instruction_text, True, (255, 255, 255))
            instruction_rect = instruction_surface.get_rect(center=(self.screen.get_width() // 2, 300))
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    self.screen.blit(self.font.render(instruction_text, True, outline_color),
                                     (instruction_rect.x + dx, instruction_rect.y + dy))
            self.screen.blit(self.font.render(instruction_text, True, shadow_color),
                             (instruction_rect.x + 2, instruction_rect.y + 2))
            self.screen.blit(instruction_surface, instruction_rect)

            pygame.display.flip()

        return self.text_input_value


class MainWindow:
    def __init__(self, screen, pet_type, pet_name, background_color):
        self.screen = screen
        self.pet_type = pet_type
        self.pet_name = pet_name
        self.background_color = background_color
        self.font = pygame.font.Font("8bitOperatorPlus8-Regular.ttf", 19)
        self.pet_status = {
            "Happiness": 100,
            "Tiredness": 50,
            "Hunger": 80,
            "Cleanliness": 90
        }
        self.last_time = time.time()

        self.show_special_message = self.pet_type.lower() == "cat" and self.pet_name.lower() == "zelda"

    def run(self):
        running = True
        while running:
            current_time = time.time()
            if current_time - self.last_time >= 300:
                self.decrease_status()
                self.last_time = current_time

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_button_click(event.pos)

            self.screen.fill(self.background_color)

            pet_info_text = f"Pet Type: {self.pet_type}, Name: {self.pet_name}"
            pet_info_font_size = 24
            self.render_text_with_outline(pet_info_text, (self.screen.get_width() // 2, 100), pet_info_font_size)

            if self.show_special_message:
                special_message_text = ("You must be Sofia! I can't believe you named your pet Zelda! I hope you enjoy "
                                        "my game.")

                special_message_font_size = 13
                self.render_text_with_outline(special_message_text, (self.screen.get_width() // 2, 150),
                                              special_message_font_size)

            status_text = self.get_status_text()
            status_font_size = 19
            self.render_text_with_outline(status_text, (self.screen.get_width() // 2, 50), status_font_size)

            # Display control buttons
            self.render_control_buttons()

            pygame.display.flip()

    def render_text_with_outline(self, text, position, font_size):
        outline_color = (0, 0, 0)
        shadow_color = (0, 0, 0)
        font = pygame.font.Font("8bitOperatorPlus8-Regular.ttf", font_size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=position)
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                self.screen.blit(font.render(text, True, outline_color), (text_rect.x + dx, text_rect.y + dy))
        self.screen.blit(font.render(text, True, shadow_color), (text_rect.x + 2, text_rect.y + 2))
        self.screen.blit(text_surface, text_rect)

    def get_status_text(self):
        status_text = ""
        for status, value in self.pet_status.items():
            status_text += f"{status}: {value}, "
        return status_text[:-2]

    def render_control_buttons(self):
        button_y = 300
        buttons = ["Feed", "Sleep", "Play", "Clean"]
        for button_text in buttons:
            button_rect = pygame.Rect((self.screen.get_width() - 200) // 2, button_y, 200, 50)
            pygame.draw.rect(self.screen, (255, 182, 193), button_rect)
            pygame.draw.rect(self.screen, (150, 150, 150), button_rect, 3)
            text_surface = self.font.render(button_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
            button_y += 60

    def handle_button_click(self, pos):
        button_y = 300
        button_height = 60
        buttons = ["Feed", "Sleep", "Play", "Clean"]
        for button_text in buttons:
            button_rect = pygame.Rect((self.screen.get_width() - 200) // 2, button_y, 200, 50)
            if button_rect.collidepoint(pos):
                if button_text == "Feed":
                    self.pet_status["Hunger"] -= 10
                elif button_text == "Sleep":
                    self.pet_status["Tiredness"] -= 10
                elif button_text == "Play":
                    self.pet_status["Happiness"] += 10
                elif button_text == "Clean":
                    self.pet_status["Cleanliness"] += 10
            button_y += button_height

    def decrease_status(self):
        for status in self.pet_status:
            if status == "Tiredness" or status == "Hunger":
                self.pet_status[status] -= 10
            else:
                self.pet_status[status] -= 5
            self.pet_status[status] = max(0, self.pet_status[status])


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    startup_window = StartupWindow()
    startup_window.run()
