# Bismarck Validator

Welcome to Bismarck Validator :confetti_ball: :sparkles:

The project validates pension xsl files and prints out the errors(if
any).

## Setting up

### Backend

```
cd server
pip3 install -r requirements.txt
rethinkdb --http-port 8090
python3 install.py
FLASK_APP=app.py FLASK_DEBUG=1 flask run --port 8080
```

### Front end
TBD. Eat a :pizza: for now.
