from flask import Flask

# _name_ contains '_main_'
app = Flask(__name__)

@app.route('/') #www.mysite.com/api/
def hello_method():
    return "Hello, world!"

if __name__ == '__main__':
    app.run()


