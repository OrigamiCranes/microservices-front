import matplotlib
matplotlib.use('Agg')
import base64
import io
import pandas
import requests
import mplfinance as mpf
from flask import render_template
from app import app


@app.route('/')
def index():
    data_block = requests.get("http://localhost:5002/api").json()

    data_frame = pandas.DataFrame.from_dict(data_block, orient='columns')
    data_frame['Date'] = data_frame['Date'].values.astype(dtype='datetime64[ms]')  # for msec format
    data_frame.set_index('Date', inplace=True)

    pngImage = io.BytesIO()

    ma5 = mpf.make_addplot(data_frame['MA-5'])
    mpf.plot(data_frame, type='candle', volume=True, addplot=ma5, savefig=dict(fname=pngImage, dpi=100, pad_inches=0.25))

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

    return render_template("index.html", image=pngImageB64String)


@app.route('/history/<id>')
def history(id):
    pass