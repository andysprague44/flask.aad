"""Application entry point."""

from application.app import create_app
from application import appsettings as config

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=config.PORT)
