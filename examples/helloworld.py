import tkinter
import tkinter.ttk

import tkgame


class HelloWorld(tkgame.Entity):

    def add(self):
        self.dx = 5
        self.dy = 5
        self.id = self.game.canvas.create_text((self.x, self.y), text='Hello World')

    def update(self, events):
        for event in events:
            self.x = event.x
            self.y = event.y

        self.x += self.dx
        self.y += self.dy

        if self.x < 0:
            self.x = 0
            self.dx = -self.dx
        else:
            game_width = self.game.width
            if self.x > game_width:
                self.x = game_width
                self.dx = -self.dx

        if self.y < 0:
            self.y = 0
            self.dy = -self.dy
        else:
            game_height = self.game.height
            if self.y > game_height:
                self.y = game_height
                self.dy = -self.dy


class Game(tkgame.Game):

    def run(self):
        self.add_event_listener('<ButtonPress>')
        self.add_entity(HelloWorld(self))


class Application:

    def __init__(self, master):
        self.master = master
        self.init()
        self.game = Game(self.canvas)

    def on_button(self):
        if self.game.running:
            self.game.stop()
            self.button.configure(text='Start')
        else:
            self.button.configure(text='Stop')
            self.game.start()

    def init(self):
        self.canvas = tkinter.Canvas(self.master)
        self.canvas.grid(sticky=tkinter.NSEW)
        self.button = tkinter.ttk.Button(self.master, text='Start', command=self.on_button)
        self.button.grid(sticky=tkinter.EW)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)


def main():
    root = tkinter.Tk()
    Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
