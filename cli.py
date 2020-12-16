import npyscreen

from game import ReelGame


class ReelGameForm(npyscreen.Form):
    def afterEditing(self, *args, **kwargs):
        self.cheat_value = ""
        self.status_value = ""
        game = self.parentApp.game
        if self.mode == "reset":
            game.reset()
            self.status_value = "Reset done"
            self.current_letters.value = game.get_current_reels_letters()
        elif self.mode == "cheat":
            best_words = game.cheat()
            self.status_value = "Cheat done"
            self.cheat_value = "Best words: " + str(best_words)
        else:
            word = self.your_word.value.lower()
            score = self.parentApp.game.evaluate_word(word)
            if score == -1:
                self.status_value = f"Word '{word}' invalid"
            elif score == 0:
                self.status_value = f"Word '{word}' unexisting"
            else:
                self.status_value = f"Word '{word}' score is {score}"
        self.your_word.value = ""
        self.current_letters.value = game.get_current_reels_letters()
        self.total_score_value = game.total_score
        self.last_existing_word_value = game.last_existing_word
        self.last_not_existing_word_value = game.last_not_existing_word
        self.previous_reels_letters_value = game.previous_reels_letters
        self.number_of_existing_words_value = str(game.number_of_existing_words)
        self.set_game_stats()

    def get_stats_title(self, title: str):
        return title.ljust(15)

    def set_game_stats(self):
        values = [
            f"{self.get_stats_title('Status')} {self.status_value}",
            f"{self.get_stats_title('Total score')} {self.total_score_value}",
            f"{self.get_stats_title('# words')} {self.number_of_existing_words_value}",
            f"{self.get_stats_title('Last OK')} {self.last_existing_word_value}",
            f"{self.get_stats_title('Last no OK')} {self.last_not_existing_word_value}",
            f"{self.get_stats_title('Prev letters')} {self.previous_reels_letters_value}",
        ]
        if self.cheat_value != "":
            values.append(f"{self.get_stats_title('CHEAT!!')} {self.cheat_value}")
        self.statistics_box.values = values

    def cheat(self, *args, **kwargs):
        self.mode = "cheat"
        self.exit_editing()

    def reset_game(self, *args, **kwargs):
        self.mode = "reset"
        self.exit_editing()

    def send_word(self, *args, **kwargs):
        self.mode = "word"
        self.exit_editing()

    def exit_app(self, *args, **kwargs):
        self.parentApp.switchForm(None)

    def create(self):
        self.current_letters = self.add(npyscreen.TitleFixedText, name="Letters")
        self.current_letters.value = self.parentApp.game.get_current_reels_letters()
        self.your_word = self.add(npyscreen.TitleText, name="Word")
        self.nextrely += 1
        self.statistics_box = self.add(
            npyscreen.BoxTitle, name="Game stats:", max_height=9
        )
        self.statistics_box.footer = "^X: Quit; ^S: Send word; ^T: Cheat; ^R: Reset;"
        self.add_handlers(
            {
                "^S": self.send_word,
                "^X": self.exit_app,
                "^R": self.reset_game,
                "^T": self.cheat,
            }
        )
        self.mode = "word"
        self.status_value = "Waiting for word"
        self.total_score_value = "0"
        self.last_existing_word_value = ""
        self.last_not_existing_word_value = ""
        self.previous_reels_letters_value = ""
        self.number_of_existing_words_value = "0"
        self.cheat_value = ""


class ReelGameCLI(npyscreen.NPSAppManaged):
    def onStart(self):
        game: ReelGame = ReelGame()
        game.load_data_from_files()
        self.game = game
        self.addForm("MAIN", ReelGameForm, name="Reel game!")


if __name__ == "__main__":
    TestApp = ReelGameCLI().run()
