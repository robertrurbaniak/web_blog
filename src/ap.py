from flask import Flask, render_template


# _name_ contains '_main_'
app = Flask(__name__)

@app.route('/') #www.mysite.com/api/
def hello_method():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(port=4999)


