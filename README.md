# flask-forum
*This repo implements a shop web application using **Flask** that is a micro-framework foundation on **Python***

### Requirements
**Python 3.8+**

#### Usage:
```
    1.Create venv via: python3 -m venv venv
    2.Install the requirements package: pip install -r requirements.txt
```

#### Simple Example


    # save this as app.py
    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello, World!"


- - -

```
$ flask run
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
