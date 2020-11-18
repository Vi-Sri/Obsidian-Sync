import rumps
class ObsidianSync(object):
    def __init__(self):
        self.config = {
            "app_name": "ObsidianSync",
            "start": "Auto Sync",
            "pause": "Sync Now",
            "continue": "Continue Sync",
            "message": "Sync mode",
            "interval": 1500
        }
        self.app = rumps.App(self.config["app_name"])
        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = self.config["interval"]
        self.set_up_menu()
        self.start_pause_button = rumps.MenuItem(title=self.config["start"], callback=self.start_timer)
        self.stop_button = rumps.MenuItem(title=self.config["stop"], callback=None)
        self.app.menu = [self.start_pause_button, self.stop_button]

    def run(self):
        self.app.run()

if __name__ == '__main__':
    app = PomodoroApp()
    app.run()