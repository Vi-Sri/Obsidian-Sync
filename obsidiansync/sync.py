import click
import daemon
import rumps
import git


class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("--")
       
