import random
from scene import Scene
from model import ProceduralBuilding
from pyglm import glm   # same as the rest of the template


class ProceduralCity(Scene):
    def __init__(self, app,
                 seed=42,
                 grid_size=40,
                 cell_size=5.5,
                 density=0.82,
                 height_variation=32.0,
                 max_height=70.0):
        # Set parameters BEFORE calling super().__init__ (important!)
        self.seed = seed
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.density = density
        self.height_variation = height_variation
        self.max_height = max_height

        random.seed(self.seed)
        super().__init__(app)   # this calls load()

    def load(self):
        add = self.add_object
        app = self.app

        # Dark cyberpunk concrete ground
        ground_scale = self.grid_size * self.cell_size * 0.5
        add(ProceduralBuilding(app,
                               pos=(0, -0.1, 0),
                               scale=(ground_scale, 0.2, ground_scale),
                               color=(0.12, 0.12, 0.15)))

        # Generate heightmap (seeded noise)
        height_map = [[0.0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                n = (random.random() * 2 - 1) * 0.6
                n += (random.random() * 2 - 1) * 0.3
                n += (random.random() * 2 - 1) * 0.1
                height_map[i][j] = (n + 1.0) / 2.0

        # Simple smoothing
        for _ in range(2):
            for i in range(1, self.grid_size - 1):
                for j in range(1, self.grid_size - 1):
                    height_map[i][j] = (height_map[i][j] +
                                        height_map[i-1][j] + height_map[i+1][j] +
                                        height_map[i][j-1] + height_map[i][j+1]) / 5.0

        neon_palette = [
            (0.0, 0.95, 0.85),   # cyan
            (0.95, 0.1, 0.85),   # magenta
            (0.0, 0.6, 1.0),     # electric blue
            (1.0, 0.7, 0.0),     # hot orange
        ]

        half = self.grid_size * self.cell_size / 2.0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if random.random() > self.density:
                    continue

                h = height_map[i][j] * self.height_variation + 4.0
                h = min(h, self.max_height)

                x = i * self.cell_size - half
                z = j * self.cell_size - half

                w = self.cell_size * random.uniform(0.75, 0.95)
                d = self.cell_size * random.uniform(0.75, 0.95)

                base_color = glm.vec3(0.16, 0.17, 0.20)

                # Main building
                add(ProceduralBuilding(app,
                                       pos=(x, h/2, z),
                                       scale=(w, h, d),
                                       color=base_color))

                # Optional Kowloon-style stacked upper floor
                if random.random() < 0.45:
                    stack_h = h * random.uniform(0.25, 0.45)
                    offset_x = random.uniform(-0.8, 0.8)
                    offset_z = random.uniform(-0.8, 0.8)
                    stack_color = random.choice(
                        neon_palette) if random.random() < 0.6 else base_color * 1.15
                    add(ProceduralBuilding(app,
                                           pos=(x + offset_x, h +
                                                stack_h/2, z + offset_z),
                                           scale=(w * 0.85, stack_h, d * 0.85),
                                           color=stack_color))

                # Roof neon accent
                if random.random() < 0.3:
                    add(ProceduralBuilding(app,
                                           pos=(x, h + 1.0, z),
                                           scale=(w * 0.9, 1.2, d * 0.9),
                                           color=random.choice(neon_palette)))
