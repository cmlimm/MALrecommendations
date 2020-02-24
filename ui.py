from tkinter import font as tkfont
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from utils import *
import urllib.request

class Anime():
    def __init__(self, title, title_english, title_japanese, poster_url, type,
                 episodes, rating, score, scored_by, background, studio, genre,
                 duration_min, aired_from_year):
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
                   aired_from_year=str(self.aired_from_year))
        return self.info


class App:
    def __init__(self):
        self.main_window = Tk()
        self.main_window.geometry("1280x480")
        self.main_window.title("Anime Recommendations")

        self.main_frame = Frame(self.main_window)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # anime list
        self.animes_frame = Frame(self.main_frame)
        self.animes_frame.grid(row=0, column=0, sticky=N)

        self.anime_listbox = Listbox(self.animes_frame, borderwidth=0, width=25, height=19)
        self.anime_scroll = Scrollbar(self.animes_frame, orient="vertical", command=self.anime_listbox.yview)
        self.anime_listbox.configure(yscrollcommand=self.anime_scroll.set)
        for title in title_list:
            self.anime_listbox.insert(END, title)
        self.anime_listbox.bind('<<ListboxSelect>>', self.select_anime)
        self.anime_listbox.grid(row=1, column=0)
        self.anime_scroll.grid(row=1, column=1, sticky=N+S+W)

        # chosen anime poster
        self.poster_frame = Frame(self.main_frame)
        self.poster_frame.grid(row=0, column=1, sticky=N)

        self.poster = ImageTk.PhotoImage(Image.open("MHA.jpg").resize((225, 319), Image.ANTIALIAS))
        self.poster_label = Label(self.poster_frame, image=self.poster)
        self.poster_label.grid(row=1, column=0)

        # chosen anime info
        self.info_frame = Frame(self.main_frame)
        self.info_frame.grid(row=0, column=2, sticky=N)

        self.synopsis = """The appearance of "quirks," newly discovered super powers, has been steadily increasing over the years, with 80 percent of humanity possessing various abilities from manipulation of elements to shapeshifting. This leaves the remainder of the world completely powerless, and Izuku Midoriya is one such individual.
Since he was a child, the ambitious middle schooler has wanted nothing more than to be a hero. Izuku's unfair fate leaves him admiring heroes and taking notes on them whenever he can. But it seems that his persistence has borne some fruit: Izuku meets the number one hero and his personal idol, All Might. All Might's quirk is a unique ability that can be inherited, and he has chosen Izuku to be his successor!
Enduring many months of grueling training, Izuku enrolls in UA High, a prestigious high school famous for its excellent hero training program, and this year's freshmen look especially promising. With his bizarre but talented classmates and the looming threat of a villainous organization, Izuku will soon learn what it really means to be a hero.
"""
        self.anime = Anime('Boku no Hero Academia', 'My Hero Academia', '僕のヒーローアカデミア',
                         'MHA.jpg', 'TV', 13, 'PG-13', 8.34, 835033, self.synopsis, 'Bones',
                         'Action, Comedy, School, Shounen, Super Power', 24, 2016)

        self.info_text = Text(self.info_frame, width=50, height=21, wrap=WORD)
        self.info_text.insert(1.0, self.anime.get_info())
        self.info_text.config(state=DISABLED)
        self.info_text.grid(row=1, column=0)

        # chosen anime synopsis
        self.synopsis_frame = Frame(self.main_frame)
        self.synopsis_frame.grid(row=0, column=3, sticky=N)

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

    def select_anime(self, selection):
        index = self.anime_listbox.curselection()[0]
        anime_info = dict(recommendations.loc[index, : ])
        image_synopsis = get_image_synopsis(anime_info['anime_id'])
        self.anime = Anime(anime_info['title'], anime_info['title_english'],
                           anime_info['title_japanese'], image_synopsis[0], anime_info['type'],
                           anime_info['episodes'], anime_info['rating'], anime_info['score'],
                           anime_info['scored_by'], image_synopsis[1],
                           anime_info['studio'], anime_info['genre'],
                           anime_info['duration_min'], anime_info['aired_from_year'])
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

app = App()
