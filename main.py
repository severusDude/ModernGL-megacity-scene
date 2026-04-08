import sys
import pygame as pg
import moderngl as mgl

from camera import Camera
from point_light import PointLight
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer


class SxvxnEngine:
    def __init__(self, win_size=(1280, 720)):
        pg.init()
        pg.display.set_caption("Modern GL Basics")
        self.WIN_SIZE = win_size

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context(require=330)
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.time = 0.0
        self.delta_time = 0.0
        self.background_color = (0.10, 0.12, 0.16)

        self.light = PointLight(position=(6.0, 8.0, 6.0), color=(1.0, 1.0, 1.0), intensity=1.2)
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.destroy()
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
                self.camera.use_orbit = not self.camera.use_orbit
                self.camera.set_default()

            if event.type == pg.KEYDOWN and event.key == pg.K_BACKQUOTE:
                visible = not pg.mouse.get_visible()
                pg.mouse.set_visible(visible)
                pg.event.set_grab(not visible)

            if event.type == pg.MOUSEBUTTONDOWN and self.camera.use_orbit:
                if event.button == 4:
                    self.camera.orbit_radius = max(2.0, self.camera.orbit_radius - 0.5)
                elif event.button == 5:
                    self.camera.orbit_radius = min(40.0, self.camera.orbit_radius + 0.5)

    def render(self):
        self.ctx.clear(color=self.background_color)
        self.scene_renderer.render()
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def destroy(self):
        self.mesh.destroy()
        self.scene_renderer.destroy()

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)


if __name__ == '__main__':
    app = SxvxnEngine()
    app.run()
