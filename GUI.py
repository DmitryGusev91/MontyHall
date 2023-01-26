""" The GUI of the "Monty Hall" project

This script opens a menu that introduce us to the "Monty Hall" problem, and
change itself according to the option picked by the user.

This script requires 'tkinter', 'matplotlib' and 'IO' be imported
In addition 'main.py' need to be imported as well, which includes the logical algorithm of the 'game'/

contains the following class:
    MontyHallGUI - activates the GUI
"""

from tkinter import *
from main import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import io


class MontyHallGUI:
    """The class MontyHallGUI initiate the GUI and starts the program

    The program will have a few option to choose from such as: radio buttons, buttons and input lines
    which will start the program according to the options that were chosen.
    Each transition from a 'tab' to another 'tab' (from page to page) will delete everything from the current 'tab'
    and initiate a new menu according to the options chosen before.

    :func __init__: initiate the main arguments and starts the graphical interface, later on from this fun
                    will activate other (inner) functions that determines the class work,
    """
    def __init__(self):
        """
        Initiates the main variables and starts the graphical interface
:
        :method main_window: Initiate the main window with all the buttons and variables that it have
        :method update_summary: Updates the final scores of win/lost of each mode(auto/mechanical/player)
                                for the statistic
        :method log_window: Initiate the window of the log OR the statistic (whichever is chosen)
        :method reset_game: Resets all the main variables
        :method game_window: Initiate and starts the game itself according to the mode the player choose
        """
        self.wins_with_change, self.wins_no_change, self.losses_with_change, self.losses_no_change, \
        self.games = 0, 0, 0, 0, 0
        self.log = io.StringIO()
        self.summary=io.StringIO()
        window = Tk()
        window.wm_attributes("-topmost", 1)
        window.geometry("800x400")
        window.configure(bg='light green')

        def main_window():
            """Initiate the main window with all the buttons and variables that it have

            You can pick a 'game mode' with the radio buttons (Automat/Mechanical/Player), if
            Automat then how many games you want it to play instantly.
            And change the window view by pressing buttons:
            Start-to start the game
            Reset-to reset the scores
            Show statistic-to show the statistic of played games
            Show log-show explanation about each played game
            exit-to exit the program

            :func selected: Shows input line if chosen mode is Automatic
            :func unselected: Hides input line if chosen mode isn't Automatic
            :func clear_main_menu: Deletes everything from main menu to make place for other 'tabs'

            :return: void
            """
            window.title("Monty Hall Game")
            top_frame = Frame(window, bg='light green')
            top_frame.pack()
            small_frame = Frame(window, bg='light green')
            bottom_frame = Frame(window, bg='light green', pady=50)
            bottom_frame.pack(side=BOTTOM)
            welcome_label = Label(top_frame, text='Welcome to the Monty Hall Challenge !!!',
                                    font=('Times', 30), pady=30, bg='light green')
            welcome_label.pack(side=TOP)
            self.amount = IntVar()
            self.amount.set("")
            self.radio_var = IntVar()
            self.radio_var.set(0)

            def selected():
                """Shows input line if chosen mode is Automatic"""
                amount_label.pack(side=LEFT)
                amount_input.pack(side=LEFT)

            def unselected():
                """Hides input line if chosen mode isn't Automatic"""
                amount_label.pack_forget()
                amount_input.pack_forget()

            rb1 = Radiobutton(top_frame, text='Automatic', variable=self.radio_var, value=1, bg='light green',
                              command=selected)
            rb1.pack()
            rb2 = Radiobutton(top_frame, text='Machine   ', variable=self.radio_var, value=2, bg='light green',
                              command=unselected)
            rb2.pack()
            rb3 = Radiobutton(top_frame, text='Player       ', variable=self.radio_var, value=3, bg='light green',
                              command=unselected)
            rb3.pack()
            small_frame.pack(pady=20)
            amount_input = Entry(small_frame, width=20, textvariable=self.amount)
            amount_label = Label(small_frame, text='enter amount of games', bg='light green')
            start_button = Button(bottom_frame, text="Start", command=lambda: [clear_main_menu(True), game_window()])
            start_button.pack(side=LEFT)
            reset_button = Button(bottom_frame, text="Reset", command=lambda:[unselected(),reset_game(True)])
            reset_button.pack(side=LEFT)
            show_stat_button = Button(bottom_frame, text="Show statistic",
                                    command=lambda: [clear_main_menu(False,True), log_window(True)])
            show_stat_button.pack(side=LEFT)
            show_log_button = Button(bottom_frame, text="Show log",
                                   command=lambda: [clear_main_menu(False,True), log_window(False)])
            show_log_button.pack(side=LEFT)
            exit_button = Button(bottom_frame, text="Exit", command=window.destroy)
            exit_button.pack(side=LEFT)
            self.errorMsg = StringVar()
            self.error_label = Label(window, fg='red', textvariable=self.errorMsg, bg='light green')
            self.error_label.pack(side=TOP)

            def clear_main_menu(start_game, stat=False):
                """Deletes everything from main menu to make place for other 'tabs'

                :param start_game: a flag that determines if the game is automatic or not . If yes then no need to
                                   clear the menu.
                :type start_game: bool
                :param stat: a flag that determines if the next menu is statistic or log. if yes the score shouldn't be
                             deleted
                :type stat: bool
                """
                # if the play was pressed and the radio button was on default(0) or Automat then don't
                # destroy everything but start unselected func that removes the input line
                if self.radio_var.get() in (0, 1) and start_game:
                    unselected()
                    return
                rb1.destroy()
                rb2.destroy()
                rb3.destroy()
                start_button.destroy()
                reset_button.destroy()
                show_stat_button.destroy()
                show_log_button.destroy()
                exit_button.destroy()
                amount_input.destroy()
                amount_label.destroy()
                amount_input.destroy()
                top_frame.destroy()
                small_frame.destroy()
                bottom_frame.destroy()
                welcome_label.destroy()
                self.error_label.destroy()
                self.errorMsg.set('')
                # resets all the scores unless it is for log or statistic and then we need the score
                if not stat:
                    reset_game()

        def update_summary():
            """Updates the final scores of win/lost of each mode(auto/mechanical/player) for the statistic

            Deletes the previous buffer and writes the current scores for the statistics
            """
            self.summary.close()
            self.summary=io.StringIO()

            self.summary.write("number of games: " + "{0:,d}".format(self.games))
            self.summary.write("\nnumber of wins because of choice change: " + "{0:,d}".format(self.wins_with_change))
            self.summary.write(
                "\nnumber of losses because of choice change: " + "{0:,d}".format(self.losses_with_change))
            self.summary.write("\nnumber of wins without the choice change: " + "{0:,d}".format(self.wins_no_change))
            self.summary.write("\nnumber of losses without the choice change: " + "{0:,d}".format(self.losses_no_change))

        def log_window(statistic):
            """Initiate the window of the log OR the statistic (whichever is chosen)

            If chosen log then shows the log window with information about each game.
            If chosen Statistic window, shows information about total amount of games in Automat mode.
            Have a pie chart of total amount of games if played at least once.

            :func back: Deletes every thing at this page to give space for the main menu
            :func pie_chart: Initiate and shows the pie chart of total amount of games

            :param statistic: a flag that determines if the log needs to be shown or the statistic
            :type statistic: bool
            :return: void
            """
            def back():
                """Deletes every thing at this page to give space for the main menu"""
                back_button.destroy()
                exit_button.destroy()
                head_line.destroy()
                text.destroy()
                if not statistic:
                    yscroll.destroy()
                frame1.destroy()
                main_window()
                if self.games != 0 and statistic:
                    canvasbar.destroy()

            def pie_chart():
                """Initiate and shows the pie chart of total amount of games"""
                fig = plt.figure(figsize=(6, 6), dpi=100)
                fig.set_size_inches(6, 8)
                fig.set_facecolor('#90ee90')
                labels, sizes, colors = [], [], []
                if self.wins_with_change != 0:
                    labels.append('Wins with change')
                    colors.append('red')
                    sizes.append(self.wins_with_change)
                if self.losses_with_change != 0:
                    labels.append('Losses with change')
                    colors.append('yellow')
                    sizes.append(self.losses_with_change)
                if self.wins_no_change != 0:
                    labels.append('Wins without change')
                    colors.append('green')
                    sizes.append(self.wins_no_change)
                if self.losses_no_change != 0:
                    labels.append('losses without change')
                    colors.append('blue')
                    sizes.append(self.losses_no_change)
                labels = tuple(labels)
                if labels:
                    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True,
                            startangle=140)
                    plt.axis('equal')
                    canvasbar = FigureCanvasTkAgg(fig, master=window)
                    canvasbar.draw()
                    plt.close()
                    return canvasbar.get_tk_widget()

            head_line = Label(window, fg='Black', bg='light green', font=("Arial", 25))
            head_line.pack()
            frame1 = Frame(window, bg='light green')
            frame1.pack()
            back_button = Button(window, text="Back", command=back)
            back_button.pack(side=LEFT, padx=100)
            exit_button = Button(window, text="Exit", command=window.destroy)
            exit_button.pack(side=RIGHT, padx=100)
            if not statistic:
                head_line.config(text="Log Of Games")
                text = Text(frame1, width=75, height=17)
                yscroll = Scrollbar(frame1, orient=VERTICAL)
                text.configure(yscrollcommand=yscroll.set)
                yscroll.pack(side=RIGHT, fill='y')
                yscroll.config(command=text.yview)
                text.insert(END, self.log.getvalue())
            else:
                head_line.config(text="Statistic")
                text = Text(frame1, width=75, height=6)
                update_summary()
                text.insert(END, self.summary.getvalue())
                if self.games != 0:
                    canvasbar = pie_chart()
                    canvasbar.pack()

            text.pack(pady=10)
            text.configure(state='disabled')

        def reset_game(reset_radio=False):
            """Resets all the main variables

            :param  reset_radio: Is a flag that determins if the radio button should be reset.
                                 If the game started then should not be reset because the game depends on it
                                 (which mode to play)
            :type reset_radio: bool (default is False)
            """

            self.wins_with_change = 0
            self.losses_with_change = 0
            self.wins_no_change = 0
            self.losses_no_change = 0
            self.games = 0
            self.log.close()
            self.log = io.StringIO()
            self.errorMsg.set('')
            self.amount.set('')
            update_summary()
            if reset_radio:
                self.radio_var.set(0)

        def game_window():
            """Initiate and starts the game itself according to the mode the player choose and writes top buffer

            If the mode is 'Automatic' then just plays the given amount of games.
            If 'Mechanical' then plays a game with visualisation.
            If 'Player' then gives the player and opportunity to choose his own choices
            If 'Player'/'Mechanical' then gives the choice to play another game or return to main menu.

            :func create_canvas: Creates a canvas to draw a card/goat/car on it
            :func first_step: Highlights the first chosen card
            :func goat_show: Shows the goat from the cards that weren't picked
            :func second_step: Highlights the second chosen card and returns the first to normal
            :func back: Deletes everything from the window to make space for main menu
            :func final_step: Shows all the cards, tells if you won or not and writes everything to buffers
            :func third_step_player: Picks the second chosen card
            :func second_step_player: Highlights the first chosen card, picks a goat and shows it
            :func first_step_player: Gets players first choice and initiate it

            :raise TclError : If the amount entered in the amount input isn't int
            """
            if self.radio_var.get() == 1:
                try:
                    for i in range(int(self.amount.get())):
                        self.log.write("Game number: " + str(self.games+1))
                        ci, fc, sc, k = mpProblem(self.log, True)
                        if ci == sc:
                            self.wins_with_change += 1
                        elif fc == ci:
                            self.losses_with_change += 1
                        self.games += 1
                    self.error_label.config(fg='blue')
                    self.errorMsg.set('Finished playing '+str(self.amount.get())+' games. '+str(self.games)+' total.')
                    self.amount.set('')
                    self.radio_var.set(0)
                except TclError:
                    self.error_label.config(fg='red')
                    self.errorMsg.set('Can accept only numbers !!!')
            elif self.radio_var.get() == 0:
                self.error_label.config(fg='red')
                self.errorMsg.set('Need to pick one option to play the game')
            else:
                self.cardPict = PhotoImage(file="card.gif")
                self.goatPict = PhotoImage(file="goat.gif")
                self.carPict = PhotoImage(file="car.gif")
                instruction = Label(window, text='Players turn to pick a card', bg='light green')
                instruction.pack(pady=5)
                result_label = Label(window, text=' ', bg='light green', font=("Arial", 20))
                result_label.pack(pady=5)
                frame1 = Frame(window, bg='light green')
                frame1.pack(pady=15)

                def create_canvas():
                    """Creates a canvas to draw a card/goat/car on it"""
                    canvas = Canvas(frame1, bg="light green")
                    canvas.create_image(40, 53, image=self.cardPict)
                    canvas["width"] = 77
                    canvas["height"] = 102
                    canvas.pack(side=LEFT, padx=40)
                    return canvas

                def first_step():
                    """Highlights the first chosen card"""
                    instruction.config(text='The dealer shows the goat')
                    canvas_list[self.fc].configure(highlightthickness=4, highlightbackground="red", bg='red')
                    texts[self.fc].config(text="First Choice")
                    if self.radio_var.get() == 2:
                        window.after(1000, goat_show)

                def goat_show():
                    """Shows the goat from the cards that weren't picked"""
                    canvas_list[self.k].itemconfig(canvas_list[self.k].create_image(40, 53, image=self.cardPict),
                                              image=self.goatPict)
                    texts[self.k].config(text="Shown Goat")
                    if self.radio_var.get() == 2:
                        window.after(500, instruction.config(text='Players turn to pick the second time'))
                        window.after(1000, second_step)

                def second_step():
                    """Highlights the second chosen card and returns the first to normal"""
                    canvas_list[self.fc].configure(highlightthickness=0, bg="light green")
                    canvas_list[self.sc].configure(highlightthickness=4, highlightbackground="red", bg="red")
                    texts[self.sc].config(text="Second Choice")
                    if self.radio_var.get() == 2:
                        window.after(1000, final_step)

                def back(repeat):
                    """Deletes everything from the window to make space for main menu

                    :param repeat: a flag that indicates if player is playing another game or returns to window
                    :type repeat: bool
                    """
                    canvas1.destroy()
                    canvas2.destroy()
                    canvas3.destroy()
                    instruction.destroy()
                    frame1.destroy()
                    buttons_frame.destroy()
                    repeat_button.destroy()
                    back_button.destroy()
                    result_label.destroy()
                    summary_label.destroy()
                    text1.destroy()
                    text2.destroy()
                    text3.destroy()
                    del self.carPict
                    del self.cardPict
                    del self.goatPict
                    if repeat:
                        game_window()
                    else:
                        reset_game()
                        main_window()

                def final_step():
                    """Shows all the cards, tells if you won or not and writes everything to buffers"""
                    instruction.config(text='The dealer shows all the choices')
                    # In case the first and the second choices are equal and it is a car
                    # need to find index of the second(not shown) goat
                    for i in range(len(canvas_list)):
                        if i != self.ci and i != self.k:
                            break
                    canvas_list[i].itemconfig(canvas_list[i].create_image(40, 53, image=self.cardPict),
                                              image=self.goatPict)
                    # In case the first and the second choices are equal need to label the one door that remained:
                    # if car then : car , if goat then : Not chosen
                    if i != self.fc and i != self.sc and i != self.ci:
                        texts[i].config(text="Not chosen")
                    if self.ci != self.fc and self.ci != self.sc:
                        texts[self.ci].config(text="Car")

                    canvas_list[self.ci].itemconfig(canvas_list[self.ci].create_image(40, 53, image=self.cardPict),
                                              image=self.carPict)
                    repeat_button.pack(pady=5)
                    back_button.pack(pady=5)
                    if self.ci == self.sc and self.fc != self.sc:
                        self.wins_with_change += 1
                        result_label.config(text='You changed your choice and WON THE CAR !!!', fg='blue')
                    elif self.fc == self.ci and self.fc != self.sc:
                        self.losses_with_change += 1
                        result_label.config(text='You changed your choice and LOST THE CAR !!!', fg='red')
                    elif self.ci == self.sc and self.fc == self.sc:
                        self.wins_no_change += 1
                        result_label.config(text='You didn\'t chang your choice and WON THE CAR !!!', fg='blue')
                    else:
                        self.losses_no_change += 1
                        result_label.config(text='You didn\'t change your choice and LOST THE CAR !!!', fg='red')
                    self.games += 1
                    update_summary()
                    summary_label.config(text=self.summary.getvalue())

                def third_step_player(num):
                    """Picks the second chosen card

                    :param num: The second choice of the player
                    :type num: int
                    """
                    self.sc = num
                    if self.sc == self.ci:
                        tmp_card = "car"
                    else:
                        tmp_card = "goat"
                    self.log.write("\nsecond choice: "+tmp_card+"  index of second choice: " + str(self.sc) + "\n\n")
                    second_step()
                    window.after(1000, final_step)

                def second_step_player():
                    """Highlights the first chosen card, picks a goat and shows it.

                    Searches for the remaining goat after first choice , if remains two then
                    picks one randomly.
                    """
                    first_step()
                    self.log.write("\nindices of goats partition: ")
                    for i in l2:
                        self.log.write(str(i)+" ")
                    # If the second choice is the same as first choice then need to pick a random goat to show
                    if self.fc == self.ci:
                        self.k = random.choice([l2[0], l2[1]])
                    else:
                        for i in l2:
                            if i != self.fc:
                                self.k = i
                                break

                    self.log.write("\nindex of exposed goat partition: " + str(self.k))
                    window.after(1000, goat_show)
                    window.after(1000, lambda: instruction.config(text='Players turn to pick the second time'))
                    for i in range(len(canvas_list)):
                        if i == self.k:
                            canvas_list[i].unbind("<Button-1>")
                        else:
                            if i == 0:
                                canvas_list[i].bind("<Button-1>", lambda e: third_step_player(0))
                            elif i == 1:
                                canvas_list[i].bind("<Button-1>", lambda e: third_step_player(1))
                            elif i == 2:
                                canvas_list[i].bind("<Button-1>", lambda e: third_step_player(2))

                def first_step_player(num):
                    """Gets players first choice and initiate it

                    :param num: The first choice the player made
                    :type num: int
                    :return: void
                    """
                    self.fc = num
                    if self.fc == self.ci:
                        self.log.write("\nfirst choice: car   index: " + str(self.fc))
                    else:
                        self.log.write("\nfirst choice: goat   index: " + str(self.fc))
                    second_step_player()

                canvas1 = create_canvas()
                canvas2 = create_canvas()
                canvas3 = create_canvas()
                text1 = Label(window, text="", bg='light green')
                text2 = Label(window, text="", bg='light green')
                text3 = Label(window, text="", bg='light green')
                text1.place(x=200, y=210)
                text2.place(x=360, y=210)
                text3.place(x=520, y=210)
                texts = [text1, text2, text3]
                canvas_list = [canvas1, canvas2, canvas3]
                self.log.write("Game number: " + str(self.games + 1))
                buttons_frame = Frame(window, bg='', pady=10)
                buttons_frame.pack()
                repeat_button = Button(buttons_frame, text="Play again", command=lambda: back(True))
                back_button = Button(buttons_frame, text="Back", command=lambda: [reset_game(True), back(False)])
                update_summary()
                summary_label = Label(window, text=self.summary.getvalue(), bg='light green', pady=5)
                summary_label.pack(side=BOTTOM)

                if self.radio_var.get() == 2:
                    self.ci, self.fc, self.sc, self.k = mpProblem(self.log, True)
                    window.after(1000, first_step)

                elif self.radio_var.get() == 3:
                    l1 = ["goat", "car", "goat"]
                    random.shuffle(l1)
                    l2 = [0, 1, 2]
                    self.ci = l1.index("car")
                    l2.remove(self.ci)
                    self.log.write("\npartitions: ")
                    for i in range(len(canvas_list)):
                        if i == self.ci:
                            self.log.write("car ")
                        else:
                            self.log.write("goat ")
                    self.log.write("\nthe car is behind partition number: " + str(self.ci))
                    canvas1.bind("<Button-1>", lambda e: first_step_player(0))
                    canvas2.bind("<Button-1>", lambda e: first_step_player(1))
                    canvas3.bind("<Button-1>", lambda e: first_step_player(2))

        main_window()
        window.mainloop()


MontyHallGUI()
