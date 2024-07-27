import os
from flask import request, render_template, jsonify

# App Initialization
from . import create_app # from __init__ file
app = create_app(os.getenv("CONFIG_MODE"))

# Applications Routes
from .views import packages_urls, qualities_urls, resources_urls, dashboard, datasets

#Main Page
@app.route('/')
def index():
    return render_template("index.html", the_title="Main Page")

if __name__ == "__main__":
    app.run()