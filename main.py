import os
from nicegui import ui

# Import the page definitions from app.main
# This ensures that the @ui.page decorators in app/main.py are executed
# and the routes are registered with NiceGUI before ui.run() is called.
import app.main  # noqa: F401 -> Ensure app.main is imported to register pages

if __name__ in {"__main__", "__mp_main__"}:  # Recommended by NiceGUI for multiprocessing compatibility
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")  # Standard for deployment environments

    ui.run(
        host=host,
        port=port,
        title="Luxury Watch Store",
        favicon="app/static/favicon.ico",
        uvicorn_logging_level='info',
        reload=False  # Set to False for production/deployment
    )