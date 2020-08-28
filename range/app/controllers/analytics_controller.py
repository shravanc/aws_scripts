from flask import request, jsonify, render_template, url_for, request, redirect
import pandas as pd
from app.libs.config import Config
from app.helpers.analytics import Analytics


def index():
    if request.method == "POST":
        config = Config(download=True)

        form = {"prefix": request.form['prefix'], "bucket": request.form['bucket']}
        #base = "2020-06-"
        base = "2020-08-"
        arr = []
        for i in range(1,28):
            form['prefix'] = f"{base}{i:02d}"
            analytics = Analytics(config, form)
            analytics.download_logs()
        config = analytics.generate()
        csv_file = config.log_file
        df = pd.read_csv(csv_file)
        df = df[config.required]
        return render_template('show.html', tables=[df.to_html(classes='data')], titles=df.columns.values
                               , bucket=config.bucket, prefix=config.prefix)



    return render_template('index.html')
