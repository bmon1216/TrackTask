"""
Title:      run.py
Desc:       main driver file for tracktask application
"""
from tracktask import app

if __name__ == '__main__':
    app.run(debug=True)  # allows for debugging and auto-reload
