# on execution, program will fill queue with 300 prophecies.

from os import path
from urllib.parse import urljoin
from tkinter import *
from random import randint, choice
from requests import get
from bs4 import BeautifulSoup
from time import time
from csv import reader, writer
from json import load
from pytumblr import TumblrRestClient

class Timer:
# timer.

    def __init__(self):
    # init. 

        pass
        # skip.

    def Start(self):
    # start timer.

        self.start_time = time()
        # get current time and store.

    def Stop(self):
    # stop timer and return formatted elapsed time.

        self.stop_time = time()
        # get current time and store.

        exact_elapsed_time = self.stop_time - self.start_time
        self.elapsed_time = float("{:.2f}".format(exact_elapsed_time))
        # calculate and round elapsed time to 2 decimal places.

        return self.elapsed_time
        # return elapsed time. 

class TumblrBot:
# bot to interface with tumblr.

    def __init__(self):
    # init.

        secret_file = open('secret.json')
        secrets = load(secret_file)
        con_key = secrets["consumer key"]
        con_sec = secrets["consumer secret"]
        auth_tok = secrets["oauth token"]
        auth_sec = secrets["oauth secret"]
        self.blog_name = secrets["blog name"]
        secret_file.close()
        # open secret.json file, extract secret info, then close file.

        self.client = TumblrRestClient(
            con_key, 
            con_sec, 
            auth_tok, 
            auth_sec
            )
        # create tumblr client object using secret info.

    def TestClient(self):
    # get blog title to test functionality. 

        bot_blog_info = self.client.blog_info(self.blog_name)
        print(bot_blog_info["blog"]["title"])
        # display authorized user info.

    def MakeQueuePost(self, image, text):
    # create post and add it to queue. 
    # NOTE MAX QUEUE SIZE IS 300 POSTS.

        self.client.create_photo(
            blogname=self.blog_name,
            state="queue",
            data=image,
            caption=text,
            tags=[  "The Dude Medium", "Prophecy", "Programming", "Oracle",
                    "The Big Lebowski", "The Dude", "Generated Post",
                    "Software Development", "Bot"])
        # create a picture post based on entered information.

class Medium:
# 'Medium' to create prophecies.

    def __init__(self, GUI=True, verbose=False):
    # init. Turn GUI off for vocab functions.

        self.insp_file = "TheBigLebowskiScript.txt"
        self.vocab_file = "Medium_Vocabulary.csv"
        self.struct_file = "sentence_structures.csv"
        self.picture_folder = "pics"
        self.verbose = verbose
        self.word_list = []
        self.prophecy = None
        self.parts_of_speech = ["noun", "pronoun", "verb", "adjective", 
                                "adverb", "preposition", "conjunction", 
                                "interjection"]
        # init vars.
        
        if GUI == True:
        # create GUI for Medium.

            btn_clr_fg = "black"
            btn_clr_bg = "light grey"
            btn_clr_fg_active = "black"
            btn_clr_bg_active = "grey75"
            # GUI vars.

            self.window = Tk()
            self.window.title("Medium")
            # create and title window.

            prophecy_frm = Frame(master=self.window)
            controls_frm = Frame(master=self.window)
            # create frames.

            self.prophecy_txt = Text(   master=prophecy_frm,
                                        height=6, width=40,
                                        padx=5, pady=5,
                                        wrap=WORD,
                                        relief=SUNKEN,
                                        state=DISABLED)
            # prophecy text box widget.

            channel_btn = Button(   master=controls_frm,
                                    text="Channel The Dude",
                                    height=1, width=20,
                                    padx=5, pady=5,
                                    background="green", foreground="white",
                                    activebackground="darkgreen",
                                    activeforeground="white",
                                    command=self.ButtonChannel)
            # 'channel' button.

            about_button = Button(  master=controls_frm,
                                    text="About",
                                    height=1, width=9,
                                    padx=5, pady=5,
                                    background=btn_clr_bg, 
                                    foreground=btn_clr_fg,
                                    activebackground=btn_clr_bg_active,
                                    activeforeground=btn_clr_fg_active,
                                    command=self.ButtonAbout)
            # 'about' button.

            exit_btn = Button(  master=controls_frm,
                                text="Exit",
                                height=1, width=9,
                                padx=5, pady=5,
                                background=btn_clr_bg, 
                                foreground=btn_clr_fg,
                                activebackground=btn_clr_bg_active,
                                activeforeground=btn_clr_fg_active,
                                command=self.ButtonExit)
            # 'exit' button. 

            self.prophecy_txt.grid(row=0,column=0)
            # place prophecy text box widget in grid.

            channel_btn.grid(   row=0, column=1,
                                padx=2.5, pady=5)
            about_button.grid(  row=0, column=0,
                                padx=2.5, pady=5)
            exit_btn.grid(      row=0, column=2,
                                padx=2.5, pady=5)
            # place control widgets in grid.

            prophecy_frm.grid(  row=0, column=0,
                                padx=5, pady=5)
            controls_frm.grid(  row=1, column=0)
            # place frames in grid.

            self.window.mainloop()
            # start GUI.

        else:
            self.tumblr = TumblrBot()
        # create tumblr client.

    def GenerateVocabulary(self):
    # generate vocabulary based on supplied .txt file.

        junk_char_list = [  "\n", ",", ".", '"', "--", "--", ":", "!", "?",
                            "(", ")", "1", "2", "3", "4", "5", "6", "7",
                            "8", "9", "0", ";", ":", "$", "-"]
        # list of junk characters. (filtered from words)

        junk_word_list = [  "walter", "sobchak", "maude", "lebowski", 
                            "theodore", "donald", "donny", "kerabatsos",
                            "brandt", "bunny", "woo", "treehorn", "uli",
                            "kunkel", "karl", "hungus", "kieffer", "franz",
                            "smokey", "marty", "jesus quintana", "liam",
                            "obrien", "terrance", "burton", "tony",
                            "voice", "over", "ralph", "ralphs", "narrator",
                            "voice--sam", "elliot's", "los", "angeles",
                            "i", "s", "t"]
        # list of junk words.

        used_word_list = []
        # list for already used words.

        if self.verbose == True:
            mainTimer = Timer()
            mainTimer.Start()
            print("** constructing vocabulary. this may take a while.")
        # display starting notification.

        raw_script = open(self.insp_file)
        script_lines = raw_script.readlines()
        current_line_number = 0
        for line in script_lines:
        # iterate over lines.

            if self.verbose == True:
                print(f"-- reading line {current_line_number} of " +
                f"{len(script_lines)}...")
                current_line_number += 1
            # display line progress.

            for word in line.split(" "):
            # iterate over words.

                for char in junk_char_list:
                    word = word.replace(char, "")
                # remove junk characters from word.

                if word.lower() in used_word_list or word.lower() in \
                    junk_word_list or len(word.replace("'", "")) <= 1:
                    continue
                used_word_list.append(word.lower())
                # filter out duplicates and words from junk word list.
                    # added new condition to filter out unexpected single char
                    # entries inadvertantly created by splitting process. 

                if self.verbose == True:
                    wordTimer = Timer()
                    wordTimer.Start()
                    print(f">> requesting {word.upper()} info...")
                # display word request notification.

                base_url = "https://www.merriam-webster.com/dictionary/"
                full_url = urljoin(base_url, word)
                dict_page = get(full_url)
                #    (f"https://www.merriam-webster.com/dictionary/{word}")
                # request dictionary page entry for word.

                if self.verbose == True:
                    elapsed_time = wordTimer.Stop()
                    print(f"<< received {word.upper()} info in approx " +
                    f"{elapsed_time} seconds.")
                # successful request confirmation.

                parsed_dict_page = BeautifulSoup(dict_page.content, 
                                                    "html.parser")
                pos_entries = parsed_dict_page.findAll("span", class_= "fl")
                # parse part of speech information from html.

                entry_list = [word.lower()]
                # create entry list containing word.

                for part in self.parts_of_speech:
                # iterate over speech types.

                    entry_pos_list = []
                    for pos in pos_entries:
                        part_of_speech = pos.text.lower()
                        for chars in junk_char_list:
                            part_of_speech = part_of_speech.replace(chars, "")
                        entry_pos_list.append(part_of_speech)
                    # filter junk characters from part of speech entries.

                    if part in entry_pos_list:
                        entry_list.append(True)
                    else:
                        entry_list.append(False)
                    # create list entry for word.

                self.word_list.append(entry_list)
                # add word entry to main word list. 

        raw_script.close()
        # close insp file.

        if self.verbose == True:
            main_elapsed_time = mainTimer.Stop()
            print(f"constructed vocabulary of {len(self.word_list)} words in" +
            f" approx {main_elapsed_time}")
        # finishing notification and timer output.

    def Memorize(self):
    # save values into csv vocab file.

        if self.verbose == True:
            memoryTimer = Timer()
            memoryTimer.Start()
        # display memorization notification.

        vocabulary = open(self.vocab_file, "w", newline= "")
        fields = ["word"]
        for pos in self.parts_of_speech:
            fields.append(pos)
        csv_writer = writer(vocabulary)
        csv_writer.writerow(fields)
        for list_entry in self.word_list:
            csv_writer.writerow(list_entry)
        vocabulary.close()
        # write list to csv file. 

        if self.verbose == True:
            elapsed_time = memoryTimer.Stop()
            print(f"memorized {len(self.word_list)} words in approx " +
            f"{elapsed_time} seconds.")
        # display memorization completion notification.

    def Think(self):
    # read stored csv vocabulary into memory. 

        vocab_file = open(self.vocab_file)
        csv_reader = reader(vocab_file)
        line_number = 0
        for words in csv_reader:
            if line_number > 0:
                self.word_list.append(words)
            line_number += 1
        vocab_file.close()
        # read vocab file contents into memory, excluding 1st line.

    def Channel(self):
    # create prophecy from memory.

        noun_list       = []
        pronoun_list    = []
        verb_list       = []
        adjective_list  = []
        adverb_list     = []
        preposition_list = []
        conjunction_list = []
        interjection_list = []
        for pos in self.word_list:
            if pos[1] == "True":
                noun_list.append(pos[0])
            if pos[2] == "True":
                pronoun_list.append(pos[0])
            if pos[3] == "True":
                verb_list.append(pos[0])
            if pos[4] == "True":
                adjective_list.append(pos[0])
            if pos[5] == "True":
                adverb_list.append(pos[0])
            if pos[6] == "True":
                preposition_list.append(pos[0])
            if pos[7] == "True":
                conjunction_list.append(pos[0])
            if pos[8] == "True":
                interjection_list.append(pos[0])
        # create and fill list of words sorted from word list. 

        raw_struct_file = open(self.struct_file)
        structures_list = reader(raw_struct_file)
        example_structures = []
        for lines in structures_list:
            example_structures.append(lines)
        model_structure = choice(example_structures)
        # select random sentence structure from csv file as model.

        rough_prophecy = []
        for item in model_structure:
            if item == "noun":
                word = choice(noun_list)
            elif item == "pronoun":
                word = choice(pronoun_list)
            elif item == "verb":
                word = choice(verb_list)
            elif item == "adjective":
                word = choice(adjective_list)
            elif item == "adverb":
                word = choice(adverb_list)
            elif item == "preposition":
                word = choice(preposition_list)
            elif item == "conjunction":
                word = choice(conjunction_list)
            else:
                word = choice(interjection_list)
            rough_prophecy.append(word)
        raw_struct_file.close()
        rough_prophecy[0] = rough_prophecy[0].capitalize()
        rough_prophecy[-1] = rough_prophecy[-1] + "..."
        self.prophecy = " ".join(rough_prophecy)
        # create prophecy according to model sentence structure. capitalizes
        # first letter and ends with elipses (to be mysterious).

    def ButtonChannel(self):
    # perform GUI channel on button click.

        if len(self.word_list) == 0:
            self.Think()
        # load words into memory, but only if list is curently empty. this 
        # prevents unneccessarily overlaoding word list from repeated presses.

        self.Channel()
        # generate prophecy from memory.

        self.prophecy_txt.config(state=NORMAL)
        # enable editing of prophecy_txt widget.

        self.prophecy_txt.delete("1.0", "6.40")
        # clear txt field for new entry.

        self.prophecy_txt.insert("1.0", self.prophecy)
        # set prophecy text to generated prophecy.

        self.prophecy_txt.config(state=DISABLED)
        # disable editing of prophecy_txt widget.

    def ButtonAbout(self):
    # display 'about' text.

        about_message = "This program was inspired by the Oracle " + \
                        "program written by Terry Davis. Rest in " + \
                        "peace, Terry. Please consider donating " + \
                        "to a local nonprofit to help those " + \
                        "struggling with mental illness. " + \
                        "\t\t\t\t\t\t\t-Snailz"
        # 'about' message to be displayed.
        ## formatted this way because i dont like how the """ method looks in
        ## this script.

        self.prophecy_txt.config(state=NORMAL)
        # enable editing of prophecy_txt widget.

        self.prophecy_txt.delete("1.0", "6.40")
        # clear txt field for new entry.

        self.prophecy_txt.insert("1.0", about_message)
        # set prophecy text to generated prophecy.

        self.prophecy_txt.config(state=DISABLED)
        # disable editing of prophecy_txt widget.

    def ButtonExit(self):
    # close program.

        self.window.destroy()
        exit()
        # close window and exit.

    def FillQueue(self):
    # create random posts and add to tumblr queue.
    # NOTE max queue size is 300.

        NUMBER_OF_POSTS = 300
        # number of posts to generate.

        self.Think()
        # load words into memory.

        for x in range(NUMBER_OF_POSTS):
        # iter ___ times.

            self.Channel()
            # create prophecy from memory.

            pic_title = f"{randint(2, 461)}.png"
            pic_path = path.join(self.picture_folder, pic_title)
            # create image title. 2 and 461 cause i trimmed some bad frames
            # from the beginning and end.

            self.tumblr.MakeQueuePost(pic_path, self.prophecy)
            # add post to queue.

            print(f"created post number {x + 1}.")
            # display confirmation statement.

TheMedium = Medium()