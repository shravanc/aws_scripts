
from lib.downloader import Downloader
from lib.parser     import Parser
from lib.analyser   import Analyser
from lib.mailer     import Mailer

class Analytics:

    def __init__(self, config):
        self.config = config

        self.downloader = Downloader(config)
        self.parser = Parser(config)
        self.analyser = Analyser(config)

    def generate_report(self):
        if self.config.download:
            self.downloader.download()
        self.parser.parse()
        self.analyser.analyse()
        return self.config

