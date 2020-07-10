from tkinter import font as tkfont
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
from utils import *
from recommendations_engine import *
import urllib.request

class Anime():
    def __init__(self, pred_score, title, title_english, title_japanese, poster_url, type,
                 episodes, rating, score, scored_by, background, studio, genre,
                 duration_min, aired_from_year):
        self.pred_score = pred_score
        self.title = title
        self.title_english = title_english
        self.title_japanese = title_japanese
        self.poster_url = poster_url
        self.type = type
        self.episodes = episodes
        self.rating = rating
        self.score = score
        self.scored_by = scored_by
        self.background = background
        self.studio = studio
        self.genre = genre
        self.duration_min = int(duration_min)
        self.aired_from_year = int(aired_from_year)

    def get_info(self):
        self.info = """Title: {title}
English title: {title_english}
Japanese title: {title_japanese}
Type: {type}
Episodes: {episodes}
Rating: {rating}
Score: {score} scored by {scored_by} people
Studio: {studio}
Genre: {genre}
Episode duration: {duration_min}
Aired: {aired_from_year}
Predicted score: {pred_score}
        """.format(title=self.title,
                   title_english=self.title_english,
                   title_japanese=self.title_japanese,
                   type=self.type,
                   episodes=str(self.episodes),
                   rating=str(self.rating),
                   score=str(self.score),
                   scored_by=str(self.scored_by),
                   studio=self.studio,
                   genre=self.genre,
                   duration_min=str(self.duration_min),
                   aired_from_year=str(self.aired_from_year),
                   pred_score = str(self.pred_score))
        return self.info

class App:
    def __init__(self):
        self.main_window = Tk()
        self.main_window.geometry("1280x480")
        self.main_window.title("Anime Recommendations")

        self.main_frame = Frame(self.main_window)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.base_recommendations = animesDF
        self.recommendations = self.base_recommendations
        self.chosen_genre_mask = [0]*39
        self.genre_flag = []

        # anime list
        self.animes_frame = Frame(self.main_frame)
        self.animes_frame.grid(row=0, column=0, sticky=N)

        self.load_list_button = Button(self.animes_frame, text='Load list', width=20, height=1, command=self.load_file)
        self.load_list_button.grid(row=2, column=0, pady=5)

        self.anime_listbox = Listbox(self.animes_frame, borderwidth=0, width=25, height=19)
        self.anime_scroll = Scrollbar(self.animes_frame, orient="vertical", command=self.anime_listbox.yview)
        self.anime_listbox.configure(yscrollcommand=self.anime_scroll.set)

        self.title_list = list(self.recommendations['title'])
        for title in self.title_list:
            self.anime_listbox.insert(END, title)
        self.anime_listbox.bind('<<ListboxSelect>>', self.select_anime)
        self.anime_listbox.grid(row=1, column=0)
        self.anime_scroll.grid(row=1, column=1, sticky=N+S+W)

        # chosen anime poster
        self.poster_frame = Frame(self.main_frame)
        self.poster_frame.grid(row=0, column=1, sticky=N)

        self.choose_genre_button = Button(self.poster_frame, text='Choose genre', width=20, height=1)
        self.choose_genre_button.config(command=self.choose_genre_gui)
        self.choose_genre_button.grid(row=2, column=0, pady=5)

        self.poster = ImageTk.PhotoImage(Image.open("MHA.jpg").resize((225, 319), Image.ANTIALIAS))
        self.poster_label = Label(self.poster_frame, image=self.poster)
        self.poster_label.grid(row=1, column=0)

        # chosen anime info
        self.info_frame = Frame(self.main_frame)
        self.info_frame.grid(row=0, column=2, sticky=N)

        self.choose_year_frame = Frame(self.info_frame)
        self.choose_year_frame.grid(row=2, column=0, pady=5)

        self.choose_year_label = Label(self.choose_year_frame, text='From year')
        self.choose_year_label.grid(row=0, column=0)

        self.choose_year_combobox = ttk.Combobox(self.choose_year_frame,
                                                 state="readonly",
                                                 values=list(range(1945, 2019)),
                                                 width=10)
        self.choose_year_combobox.current(0)
        self.choose_year_combobox.bind('<<ComboboxSelected>>', self.update_recommendations)
        self.choose_year_combobox.grid(row=0, column=1)

        self.synopsis = """Press "Load button" to load your anime list from My Anime List converted to CSV
Press recommend to get recommendations
Press choose genre to choose genre
Choose minimal year
Enjoy!
"""
        self.anime = Anime(10, 'Anime Recommendations App', 'Anime Recommendations App', 'アニメおすすめアプリ',
                         'MHA.jpg', 'Desktop', 1, 'PG-13', 10, 1, self.synopsis, 'SPbSUE',
                         'Coursework, Comedy, University, Super Power', 4320, 2020)

        self.info_text = Text(self.info_frame, width=50, height=21, wrap=WORD)
        self.info_text.insert(1.0, self.anime.get_info())
        self.info_text.config(state=DISABLED)
        self.info_text.grid(row=1, column=0)

        # chosen anime synopsis
        self.synopsis_frame = Frame(self.main_frame)
        self.synopsis_frame.grid(row=0, column=3, sticky=N)

        self.recommend_button = Button(self.synopsis_frame, text='Recommend', width=20, height=1, command=self.recommend)
        self.recommend_button.grid(row=2, column=0, pady=5)

        self.reset_button = Button(self.synopsis_frame, text='Reset', width=20, height=1, command=self.reset)
        self.reset_button.grid(row=3, column=0, pady=5)

        self.synopsis_text = Text(self.synopsis_frame, width=50, height=21, wrap=WORD)
        self.synopsis_text.insert(1.0, self.anime.background)
        self.synopsis_scroll = Scrollbar(self.synopsis_frame,
                                         command=self.synopsis_text.yview,
                                         orient="vertical")
        self.synopsis_text.config(yscrollcommand=self.synopsis_scroll.set)
        self.synopsis_text.config(state=DISABLED)

        self.synopsis_scroll.grid(row=1, column=1, sticky=N+S+W)
        self.synopsis_text.grid(row=1, column=0)

        # column names
        self.animes_column_label = Label(self.animes_frame, text='Recommended anime')
        self.poster_column_label = Label(self.poster_frame, text='Poster')
        self.info_column_label = Label(self.info_frame, text='Information')
        self.synopsis_column_label = Label(self.synopsis_frame, text='Synopsis')

        self.animes_column_label.grid(row=0, column=0)
        self.poster_column_label.grid(row=0, column=0)
        self.info_column_label.grid(row=0, column=0)
        self.synopsis_column_label.grid(row=0, column=0)

        self.main_window.mainloop()

    # updates displayed anime
    def select_anime(self, event=None):
        try:
            self.index = self.anime_listbox.curselection()[0]
            self.anime_info = dict(self.recommendations.loc[self.index, : ])

            # get image and synopsis bc image url's are broken in this dataset
            # and there is no synopsis
            self.image_synopsis = get_image_synopsis(self.anime_info['anime_id'])

            try:
                # if there is no recommendations made
                pred_score = round(self.anime_info['pred_score'], 2)
            except:
                pred_score = 'No predicted score'

            self.anime = Anime(pred_score, self.anime_info['title'], self.anime_info['title_english'],
                               self.anime_info['title_japanese'], self.image_synopsis[0], self.anime_info['type'],
                               self.anime_info['episodes'], self.anime_info['rating'], self.anime_info['score'],
                               self.anime_info['scored_by'], self.image_synopsis[1],
                               self.anime_info['studio'], self.anime_info['genre'],
                               self.anime_info['duration_min'], self.anime_info['aired_from_year'])

            self.info_text.config(state=NORMAL)
            self.info_text.delete("1.0", "end")
            self.info_text.insert(1.0, self.anime.get_info())
            self.info_text.config(state=DISABLED)

            self.synopsis_text.config(state=NORMAL)
            self.synopsis_text.delete("1.0", "end")
            self.synopsis_text.insert(1.0, self.anime.background)
            self.synopsis_text.config(state=DISABLED)

            self.poster = ImageTk.PhotoImage(Image.open(urllib.request.urlopen(self.anime.poster_url)).resize((225, 319), Image.ANTIALIAS))
            self.poster_label.config(image = self.poster)
        except Exception as ex:
            print(ex)

    # genre selection
    def choose_genre_gui(self):
        self.genre_window = Toplevel()
        self.genre_window.geometry("220x480")
        self.genre_window.title("Choose genre")

        self.genre_flag = {}
        self.genre_buttons = {}

        # create checkbutton for every genre
        for i in range(39):
            self.genre_flag[i]= IntVar()
            if self.chosen_genre_mask[i] == 0:
                self.genre_flag[i].set(0)
            else:
                self.genre_flag[i].set(1)
            self.genre_buttons[i] = Checkbutton(self.genre_window, text=genre_list[i], variable=self.genre_flag[i])
            if i <= 20:
                self.genre_buttons[i].grid(row=i, column=0, sticky=W)
            else:
                self.genre_buttons[i].grid(row=i-21, column=1, sticky=W)

        # save and exit button
        self.ok_genre_button = Button(self.genre_window, text='Ok', width=7, height=1, command=self.close_genre_gui)
        self.ok_genre_button.grid(row=19, column=1)

        self.reset_genre_button = Button(self.genre_window, text='Reset', width=7, height=1, command=self.reset_genre)
        self.reset_genre_button.grid(row=20, column=1)

        self.genre_window.mainloop()

    # closes window with genres and updates recommendations according to selected genres
    def close_genre_gui(self, event=None):
        self.update_recommendations()
        self.genre_window.destroy()

    # makes all genre unselected
    def reset_genre(self, event=None):
        if self.genre_flag != []:
            for i in range(39):
                self.genre_flag[i].set(0)

    def update_recommendations(self, event=None):
        self.recommendations = self.base_recommendations
        if self.genre_flag != []:

            # find names of selected genres
            self.chosen_genre_mask = [1 if self.genre_flag[i].get() == 1 else 0 for i in range(39)]
            self.chosen_genre = [genre_list[i] for i in range(39) if self.genre_flag[i].get() == 1]

            # find animes that have these genres
            self.regexp = ''.join(['(?=.*{}.*)'.format(genre) for genre in self.chosen_genre])
            self.recommendations = self.recommendations[(self.recommendations.genre.str.contains(self.regexp, regex=True))]

        # find animes that aired after selected year
        self.recommendations = self.recommendations[self.recommendations.aired_from_year >= int(self.choose_year_combobox.get())]

        self.recommendations = self.recommendations.reset_index(drop=True)
        self.title_list = list(self.recommendations['title'])
        self.anime_listbox.delete(0, END)
        for title in self.title_list:
            self.anime_listbox.insert(END, title)

    def recommend(self, event=None):
        self.base_recommendations = get_recommendations_dataframe(self.userDF, animesDF, similarity_table, anime_ids)
        self.reset_genre()
        self.choose_year_combobox.current(0)
        self.update_recommendations()

    # resets everything as if no changes were made
    def reset(self, event=None):
        self.base_recommendations = animesDF
        self.reset_genre()
        self.choose_year_combobox.current(0)
        self.update_recommendations()

    # opens file with user anime list
    def load_file(self, event=None):
        self.user_filename = filedialog.askopenfilename(initialdir="/", title="Select Anime List", filetypes=(("CSV files", "*.csv"),("all files", "*.*")))
        self.userDF = load_user_list(self.user_filename)

app = App()
