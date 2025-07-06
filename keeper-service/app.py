from flask import Flask
from controllers import cuentas, despensa


app = Flask(__name__)

app.register_blueprint(cuentas)
app.register_blueprint(despensa)



if __name__ == '__main__':
    app.run(port=8003, debug=True)