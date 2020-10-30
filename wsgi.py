"""App entry point."""
from movie_web_app import create_app
from flask_wtf.csrf import CSRFProtect

app = create_app()

if __name__ == "__main__":

    app.run(host='localhost', port=5000, threaded=False)