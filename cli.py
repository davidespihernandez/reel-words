import npyscreen

from game import ReelGame


class ReelGameForm(npyscreen.Form):
    def afterEditing(self):
        word = self.your_word.value
        self.cheat.value = ""
        if word == "/reset":
            self.parentApp.game.reset()
            self.status.value = "Reset done"
            self.current_letters.value = self.parentApp.game.get_current_reels_letters()
        elif word == "/cheat":
            best_words = self.parentApp.game.cheat()
            self.status.value = "Cheat done"
            self.cheat.value = "Best words: \n" + str(best_words)
        else:
            score = self.parentApp.game.evaluate_word(self.your_word.value)
            self.status.value = f"Word {self.your_word.value} score is {score}"
            self.your_word.value = ""
        self.current_letters.value = self.parentApp.game.get_current_reels_letters()

    def create(self):
        self.status = self.add(npyscreen.TitleFixedText, name="Status")
        self.current_letters = self.add(npyscreen.TitleFixedText, name="Letters")
        self.current_letters.value = self.parentApp.game.get_current_reels_letters()
        self.your_word = self.add(npyscreen.TitleText, name="Word")
        self.cheat = self.add(npyscreen.TitleFixedText, name="Cheat")


class ReelGameCLI(npyscreen.NPSAppManaged):
    def onStart(self):
        game: ReelGame = ReelGame()
        game.load_data_from_files()
        self.game = game
        self.addForm("MAIN", ReelGameForm, name="Reel game!")


if __name__ == "__main__":
    TestApp = ReelGameCLI().run()
