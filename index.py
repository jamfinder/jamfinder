from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    #detect user IP
    print request.access_route

    return render_template('hello.html', name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()

if __name__ == '__main__':
    app.run()
