import tkinter as tk
import random
import json
import os
import sys

class SceneGenerator:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)
        file_path = os.path.join(application_path, 'story_elements.json')
        with open(file_path, 'r') as file:
            self.matrix = json.load(file)

    def generate_introduction_scene(self, player_state):
        person = random.choice(self.matrix['people'])
        place = random.choice(self.matrix['places']['urban_places'])
        theme = random.choice(self.matrix['themes'])
        weather = random.choice(self.matrix['weather'])
        player_state['theme'] = theme
        return f"It's a {weather} day. You encounter {person} at {place}. Your adventure of {theme} begins."

    def generate_rising_action_scene(self, player_state):
        action = random.choice(self.matrix['actions'])
        place = random.choice(self.matrix['places']['natural_places'])
        object_ = random.choice(self.matrix['objects'])
        return f"You decide to {action} {place}. Along the way, you discover {object_}. Tension is building."

    def generate_climax_scene(self, player_state):
        event = random.choice(self.matrix['events'])
        object_ = random.choice(self.matrix['objects'])
        return f"You {event}. The pivotal moment revolves around {object_}. Everything is at stake."

    def generate_falling_action_scene(self, player_state):
        action = random.choice(self.matrix['actions'])
        place = random.choice(self.matrix['places']['special_places'])
        return f"You {action} {place}. The conflicts are starting to resolve."

    def generate_conclusion_scene(self, player_state):
        character = random.choice(self.matrix['people'])
        theme = player_state['theme']
        return f"You reflect on your journey with {character}. The story of {theme} reaches its conclusion."

class Game:
    def __init__(self):
        self.scene_generator = SceneGenerator()
        self.current_scene = 'start'
        self.player_state = {'theme': None}
        self.scenes = {
            'start': {
                'choices': ["Explore the city", "Reflect on your life"],
                'choice1': {'text': "You immerse yourself in urban culture.", 'next_scene': 'rising_action'},
                'choice2': {'text': "You spend the day reflecting.", 'next_scene': 'rising_action'},
            },
            'rising_action': {
                'choices': ["Investigate a mystery", "Pursue an adventure"],
                'choice1': {'text': "You delve into the unknown.", 'next_scene': 'climax'},
                'choice2': {'text': "You embark on a grand adventure.", 'next_scene': 'climax'},
            },
            'climax': {
                'choices': ["Face the challenge", "Retreat and rethink"],
                'choice1': {'text': "You confront the challenge head-on.", 'next_scene': 'falling_action'},
                'choice2': {'text': "You retreat to strategize.", 'next_scene': 'falling_action'},
            },
            'falling_action': {
                'choices': ["Reflect on the journey", "Prepare for the next adventure"],
                'choice1': {'text': "You reflect on what you've learned.", 'next_scene': 'end_of_day'},
                'choice2': {'text': "You prepare for your next journey.", 'next_scene': 'end_of_day'},
            },
            'end_of_day': {
                'choices': ["Move to the next day", "End the game"],
                'choice1': {'text': "A new day begins!", 'next_scene': 'start'},
                'choice2': {'text': "Thank you for playing!", 'next_scene': 'end_game'},
            }
        }

    def make_choice(self, scene, result_label, update_buttons):
        result_label.config(text=self.scenes[self.current_scene][scene]['text'])
        self.current_scene = self.scenes[self.current_scene][scene]['next_scene']
        update_buttons()

    def get_scene_text(self):
        scene_method = {
            'start': self.scene_generator.generate_introduction_scene,
            'rising_action': self.scene_generator.generate_rising_action_scene,
            'climax': self.scene_generator.generate_climax_scene,
            'falling_action': self.scene_generator.generate_falling_action_scene,
            'end_of_day': self.scene_generator.generate_conclusion_scene
        }
        return scene_method[self.current_scene](self.player_state)

class SeandruhApp:
    def __init__(self, root):
        self.game = Game()
        self.root = root
        self.root.title("Seandruh")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Welcome to Seandruh, a game of exploration.").pack()
        self.scene_label = tk.Label(self.root, text="")
        self.scene_label.pack()
        self.buttons = [
            tk.Button(self.root, text="", command=lambda: self.game.make_choice('choice1', self.result_label, self.update_buttons)),
            tk.Button(self.root, text="", command=lambda: self.game.make_choice('choice2', self.result_label, self.update_buttons))]
        for button in self.buttons:
            button.pack()
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()
        self.update_buttons()

    def update_buttons(self):
        scene_text = self.game.get_scene_text()
        self.scene_label.config(text=scene_text)
        for i, button in enumerate(self.buttons):
            if self.game.scenes[self.game.current_scene]['choices'][i]:
                button.config(text=self.game.scenes[self.game.current_scene]['choices'][i], state=tk.NORMAL)
            else:
                button.config(state=tk.DISABLED)
        if self.game.current_scene == 'end_game':
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SeandruhApp(root)
    root.mainloop()


