from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.widgets import *
import sys

from game import Game

class MainView(Frame):
    def __init__(self, screen):
        super(MainView, self).__init__(screen,
                                        8,  #Frame Height
                                        16, #Frame Width
                                        hover_focus=True,
                                        can_scroll=False,
                                        title="Main Menu")

        #Widget Palette-----------
        #self.palette['object'] = (foreground, ???, background) I just leave the 2nd item as 2. 3 inverts the colors.
        self.palette['label'] = (7,2,4)
        self.palette['disabled'] = (0,2,4)
        self.palette['focus_button'] = (0,2,2)

        #Objects in Frame---------
        layout = Layout([0,1,0], fill_frame=False)

        self._title_label = Label("Tic-Tac-Toe", align="^")
        self._start_button = Button("Start Game", self.startGame)
        self._quit_button = Button("Quit", self._quit)

        self.add_layout(layout)
        #-------------------------


        #Formatting---------------
        layout.add_widget(Divider(draw_line=False),1)
        layout.add_widget(self._title_label, 1)
        layout.add_widget(Divider(draw_line=False),1)
        layout.add_widget(Divider(draw_line=False),1)
        layout.add_widget(self._start_button, 1)
        layout.add_widget(self._quit_button, 1)
        self.fix()
        #-------------------------
    

    def startGame(self):
        raise NextScene("Game") #Starts the game

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["No", "Yes"],
                        self._quit_on_yes)
        )

    def _quit_on_yes(self,dec):
        if dec:
            sys.exit()


class GameView(Frame):
    def __init__(self, screen, game):
        super(GameView, self).__init__(screen,
                                        8,  #Frame Height
                                        25, #Frame Width
                                        hover_focus=True,
                                        can_scroll=False,
                                        title="Tic-Tac-Toe")

        self.game = game    #Instanciating the Game class
        self.win = "N"

        #Objects in Frame---------
        layout = Layout([1,0.25,1,0.25,1,0.25,2], fill_frame=False)
        layout2 = Layout([2,3,1])

        self._button_grid = {}
        for i in range(9):
            self._button_grid[i] = Button("", lambda num=i : self.play(num), add_box=False)

        self._winner_label = Label("Winner")
        self._winner_text = Text("")
        self._turn_label = Label("Turn")
        self._turn_text = Text("",max_length=1)

        self._start_button = Button("New Game", self.newGame, add_box=False)
        self._quit_button = Button("Quit", self._quit, add_box=False)
        #-------------------------


        #Formatting---------------
        self.add_layout(layout)

        b = 0
        for i in range(15):
            if i in (0,2,4,5,7,9,10,12,14):
                layout.add_widget(self._button_grid[b], i%5)
                b+=1
            if i in (1,3) and i < 15:
                for j in range(5):
                    layout.add_widget(VerticalDivider(height=1), i%5)
            if i in (0,2,4,5,7,9):
                layout.add_widget(Divider(True,1), i%5)

        layout.add_widget(VerticalDivider(5),5)
        layout.add_widget(self._turn_label,6)
        layout.add_widget(self._turn_text, 6)
        layout.add_widget(Divider(False),6)
        layout.add_widget(self._winner_label,6)
        layout.add_widget(self._winner_text, 6)
        self._turn_text.disabled = True
        self._turn_text.value = "X" 

        self.add_layout(layout2)
        layout2.add_widget(self._start_button, 0)
        layout2.add_widget(self._quit_button, 2)
        self._start_button.disabled=True
        self._winner_text.disabled=True
        self._start_button.is_visible

        self.fix()
        #-------------------------

    def play(self,num):
        if self._button_grid[num].text in ("X","O") or self.win != "N": #If there is a mark there, or the game is over, do nothing
            return
        if self.game.turn:
            self._button_grid[num].text = "X"   #Put an X on the board at the spot selected
            self._turn_text.value = "O"
        else: 
            self._button_grid[num].text = "O" #Put an O on the board at the spot selected
            self._turn_text.value = "X"
        self.encode(num)                        #Create an (x,y) pair for the game object
        self.game.play(self.x, self.y)          #Update the internal board
        self.win = self.game.checkWinner(self.y, self.x)    #Check the internal board for a win condition
        if self.win in ("X","O"): self._start_button.disabled = False; self._winner_text.value = self.win   #Tell the user(s) who won
        if self.win == "T": self._start_button.disabled = False; self._winner_text.value = "TIE"            #Tell the user(s) no one won

    def newGame(self):
        self.game.newGame()     #Create new internal board
        for i in range(9):
            self._button_grid[i].text = "    "  #Clear all of the spaces (looks weired because of formatting issues)
            self._button_grid[i].reset()        #Resets the spaces to their original state just to be sure
        self._start_button.disabled = True
        self._turn_text.value = "X"
        self.win = "N"          #Let the user(s) play

    def encode(self,num):   #Turns a number into an ordered (x,y) pair according to a 3x3 grid
        if num in (0,1,2): self.y = 0
        if num in (3,4,5): self.y = 1
        if num in (6,7,8): self.y = 2

        if num in (0,3,6): self.x = 0
        if num in (1,4,7): self.x = 1
        if num in (2,5,8): self.x = 2

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["No", "Yes"],
                        self._quit_on_yes)
        )

    def _quit_on_yes(self,dec):
        if dec:
            sys.exit()

def demo(screen, scene):
    scenes =  [
        Scene([MainView(screen)], -1, name="Main"),
        Scene([GameView(screen, Game())], -1, name="Game")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

def main() -> None:
    last_scene = None
    while True: #The main loop
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:  #Actually clever. it takes the "code" given when raised and uses it to change to that scene.
            last_scene = e.scene

if __name__ == "__main__":
    main()