from flask import request, jsonify, render_template, url_for, request, redirect
import pandas as pd
from app.libs.config import Config
from app.helpers.analytics import Analytics

def index():
  if request.method == "POST":
    config = Config(download=False)
    analytics = Analytics(config, request)
    config = analytics.generate_report()

    csv_file = config.log_file #'/home/shravan/Desktop/logs.csv'
    df = pd.read_csv(csv_file)
    df = df[config.required]
    return render_template('show.html', tables=[df.to_html(classes='data')], titles=df.columns.values, bucket=config.bucket, prefix=config.prefix)

  return render_template('index.html')


