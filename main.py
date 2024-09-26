from flask import Flask,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    login = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50), nullable=False)


@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_correo = request.form.get('correo')
        form_password = request.form.get('contraseña')
        users_db = User.query.all()
        for user in users_db:
            if form_correo == user.login and form_password == user.contraseña:
                return redirect('index.html')
            else:
                error = 'Usuario o contraseña incorrecta'
                return render_template('login.html',error=error)
    else:
        return render_template('login.html')
    
@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        correo = request.form.get('correo') 
        password = request.form.get('contraseña')
        user = User(correo=correo,password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('reg.html')
@app.route('/index')
def index():
    return render_template('index.html',)

app.run(debug=True,host='0.0.0.0')