"""
Title:      run.py
Desc:       main driver file for TrackTask application
"""
from tracktask import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # allows for debugging and auto-reload
