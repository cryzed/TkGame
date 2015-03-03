import math
import time


class Entity:

    def __init__(self, game):
        self.game = game

        self.id = None
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.width = 0
        self.height = 0

    def add(self):
        pass

    def update(self):
        pass

    def draw(self, interpolation):
        x = self.x + self.dx * interpolation
        y = self.y + self.dy * interpolation

        if not self.width or not self.height:
            self.game.canvas.coords(self.id, (x, y))
        else:
            self.game.canvas.coords(self.id, (x, y, x+self.width, y+self.height))

    def remove(self):
        self.game.canvas.delete(self.id)


class Game:

    def __init__(self, canvas, ticks_per_second=20, frames_per_second=60, maximum_frameskip=5):
        self.canvas = canvas

        self._tick_delay = 1 / ticks_per_second
        self._frame_delay = 1 / frames_per_second
        self._maximum_frameskip = maximum_frameskip

        self.running = False
        self._next_update = None
        self._next_draw = None
        self._entities = []
        self._event_listeners = {}
        self._events = []

    @property
    def width(self):
        return self.canvas.winfo_width()

    @property
    def height(self):
        return self.canvas.winfo_height()

    def add_entity(self, entity):
        entity.add()
        self._entities.append(entity)

    def remove_entity(self, entity):
        entity.remove()
        self._entities.remove(entity)

    def start(self):
        self.running = True
        self._next_update = time.perf_counter()
        self._next_draw = self._next_update

        self.run()
        self._run()

    def pause(self):
        self.running = False

    def stop(self):
        self.running = False
        self.unregister_event_listeners(tuple(self._event_listeners.keys()))
        self._events.clear()
        for entity in self._entities:
            entity.remove()

    def run(self):
        pass

    def update(self, events):
        pass

    def draw(self):
        pass

    def _update(self):
        events = tuple(self._events)
        self.update(events)
        for entity in self._entities:
            entity.update(events)

        self._events.clear()

    def _draw(self, interpolation):
        self.draw()
        for entity in self._entities:
            entity.draw(interpolation)

    def _on_event(self, event):
        if self.running:
            self._events.append(event)

    def register_event_listeners(self, event_listeners):
        for event_listener in event_listeners:
            id_ = self.canvas.bind(event_listener, self._on_event)
            self._event_listeners[event_listener] = id_

    def unregister_event_listeners(self, event_listeners):
        for event_listener in event_listeners:
            id_ = self._event_listeners[event_listener]
            self.canvas.unbind(event_listener, id_)
            del self._event_listeners[event_listener]

    # http://www.koonsolo.com/news/dewitters-gameloop/
    # FPS are limited to 1000 and TPS to 1000 * self.maximum_frameskip
    # due to TkInter's after method only accepting integers
    def _run(self):
        if not self.running:
            return

        updates = 0
        next_update = self._next_update
        maximum_frameskip = self._maximum_frameskip
        tick_delay = self._tick_delay
        next_draw = self._next_draw

        while time.perf_counter() > next_update and updates < maximum_frameskip:
            self._update()
            updates += 1
            next_update += tick_delay
        self._next_update = next_update

        if time.perf_counter() > next_draw:
            interpolation = (time.perf_counter() + tick_delay - next_update) / tick_delay
            self._draw(interpolation)
            while time.perf_counter() > next_draw:
                next_draw += self._frame_delay
        self._next_draw = next_draw

        delay = int(math.floor(min(next_draw - time.perf_counter(), next_update - time.perf_counter()) * 1000))
        self.canvas.after(delay or 1, self._run)
