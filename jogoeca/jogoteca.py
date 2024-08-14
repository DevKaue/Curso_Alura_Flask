from flask import Flask, render_template

app = Flask(__name__)

@app.route('/initio')
def ola():
    return render_template('lista.html')

app.run()
