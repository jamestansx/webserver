import argparse
from webserver import app
from waitress import serve

parser = argparse.ArgumentParser()
parser.add_argument(
    "--flask", action="store_true", help="Use app.run() instead of waitress.serve()"
)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.flask:
        app.run(debug=True)
    else:
        serve(app, host="127.0.0.1", port=5000)
