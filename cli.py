import npyscreen

from game import ReelGame


class ReelGameForm(npyscreen.Form):
    def afterEditing(self, *args, **kwargs):
        word = self.your_word.value
        self.cheat.value = ""
        game = self.parentApp.game
        if word == "/reset":
            game.reset()
            self.status.value = "Reset done"
            self.current_letters.value = game.get_current_reels_letters()
        elif word == "/cheat":
            best_words = game.cheat()
            self.status.value = "Cheat done"
            self.cheat.value = "Best words: \n" + str(best_words)
        else:
            score = self.parentApp.game.evaluate_word(self.your_word.value)
            if score == -1:
                self.status.value = f"Word {self.your_word.value} invalid"
            elif score == 0:
                self.status.value = f"Word {self.your_word.value} unexisting"
            else:
                self.status.value = f"Word {self.your_word.value} score is {score}"
        self.your_word.value = ""
        self.current_letters.value = game.get_current_reels_letters()
        self.total_score.value = game.total_score
        self.last_existing_word.value = game.last_existing_word
        self.last_not_existing_word.value = game.last_not_existing_word
        self.previous_reels_letters.value = game.previous_reels_letters
        self.number_of_existing_words.value = str(game.number_of_existing_words)

    def send_word(self, *args, **kwargs):
        self.exit_editing()

    def exit_app(self, *args, **kwargs):
        self.parentApp.switchForm(None)

    def create(self):
        self.status = self.add(npyscreen.TitleFixedText, name="Status")
        self.current_letters = self.add(npyscreen.TitleFixedText, name="Letters")
        self.current_letters.value = self.parentApp.game.get_current_reels_letters()
        self.your_word = self.add(npyscreen.TitleText, name="Word")
        self.cheat = self.add(npyscreen.TitleFixedText, name="Cheat")
        self.total_score = self.add(npyscreen.TitleFixedText, name="Score")
        self.number_of_existing_words = self.add(
            npyscreen.TitleFixedText, name="# words"
        )
        self.last_existing_word = self.add(npyscreen.TitleFixedText, name="Last OK")
        self.last_not_existing_word = self.add(
            npyscreen.TitleFixedText, name="Last no OK"
        )
        self.previous_reels_letters = self.add(
            npyscreen.TitleFixedText, name="Prev letters"
        )
        self.add_handlers({"^S": self.send_word, "^X": self.exit_app})


class ReelGameCLI(npyscreen.NPSAppManaged):
    def onStart(self):
        game: ReelGame = ReelGame()
        game.load_data_from_files()
        self.game = game
        self.addForm("MAIN", ReelGameForm, name="Reel game!")


if __name__ == "__main__":
    TestApp = ReelGameCLI().run()
