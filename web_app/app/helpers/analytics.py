
from app.libs.s3_logs.downloader import Downloader
from app.libs.s3_logs.parser import Parser
from app.libs.s3_logs.analyser import Analyser

class Analytics:

  def __init__(self, config, request):
    self.config = config
    self.bucket = request.form.get('bucket')
    if self.bucket:
      self.config.bucket = self.bucket

    self.prefix = request.form.get('prefix')
    if self.prefix:
      self.config.prefix = self.prefix


    self.downloader = Downloader(config)
    self.parser = Parser(config)
    self.analyser = Analyser(config)

  def generate_report(self):
    if self.config.download:
      self.downloader.download()
    self.parser.parse()
    self.analyser.analyse()
    return self.config

