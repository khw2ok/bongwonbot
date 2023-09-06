from flask import Flask
from src import main
app = Flask(__name__)
app.config["SERVER_NAME"] = "b1bot.kro.kr"
app.register_blueprint(main.app)

if __name__ == "__main__":
  app.run("0.0.0.0", 5000, True)