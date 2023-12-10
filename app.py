from flask import Flask, render_template
from map import create_map

app = Flask(__name__)

# Generate the map and save it as an HTML file
create_map()

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8080) 
