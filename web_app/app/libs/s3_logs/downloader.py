import os

class Downloader:

  def __init__(self, config):
    self.bucket = config.bucket
    self.prefix = config.prefix
    self.local  = config.local_path
    self.client = config.client


  def download(self):
    keys = []
    dirs = []
    next_token = ''
    base_kwargs = {
        'Bucket': self.bucket,
        'Prefix': self.prefix,
    }


    while next_token is not None:
      kwargs = base_kwargs.copy()
      if next_token != '':
        kwargs.update({'continuationToken': next_token})
      results = self.client.list_objects_v2(**kwargs)
      contents = results.get('Contents')
      for i in contents:
        k = i.get('Key')
        if k[-1] != '/':
          keys.append(k)
        else:
          dirs.append(k)

      next_token = results.get('NextContinuationToken')

    for d in dirs:
        dest_pathname = os.path.join(self.local, d)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
    for k in keys:
        dest_pathname = os.path.join(self.local, k)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
        self.client.download_file(self.bucket, k, dest_pathname)
