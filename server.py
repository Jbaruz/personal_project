from flask_base import app
from flask_base.controllers import core, recipe

if __name__ == "__main__":
    app.run(debug=True)