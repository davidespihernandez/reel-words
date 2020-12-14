import npyscreen

from game import ReelGame


class ReelGameForm(npyscreen.Form):
    #    def afterEditing(self):
    #        self.parentApp.setNextForm(None)

    def on_ok(self):
        self.current_letters.value = "cambia"  # self.parentApp.game.selected_word([1])

    def create(self):
        self.current_letters = self.add(npyscreen.TitleFixedText, name="Letters")
        self.current_letters.value = self.parentApp.game.current_word()
        self.your_word = self.add(npyscreen.TitleText, name="Word")


class ReelGameCLI(npyscreen.NPSAppManaged):
    def onStart(self):
        game: ReelGame = ReelGame()
        game.load_data_from_files()
        self.game = game
        self.addForm("MAIN", ReelGameForm, name="Reel game!")


if __name__ == "__main__":
    TestApp = ReelGameCLI().run()
