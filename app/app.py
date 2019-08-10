# Imports:
from flask import Flask, render_template, request

# App:
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():  
  return render_template('pages/index.html')

# Server:
if __name__ == '__main__':
  app.run(debug=True)
