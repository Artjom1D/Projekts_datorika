from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
import bcrypt
# Importē nepieciešamās bibliotēkas ar funkciju pip install un bibliotēkas nosaukumu: flask flask_sqlalchemy bcrypt


# Funkcija, lai hashotu paroli un atgrieztu to kā virkni
def hashed_str(plain_text):
    return bcrypt.hashpw(plain_text.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Funkcija, lai pārbaudītu, vai ievadītā parole atbilst hash
def check_str(plain_text, hashed_str):
    if isinstance(hashed_str, str):
        hashed_str = hashed_str.encode('utf-8')  # Konvertē hash uz baitiem, ja tas ir virkne
    return bcrypt.checkpw(plain_text.encode('utf-8'), hashed_str)

app = Flask(__name__, template_folder='templates')  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)









# Funkcija, lai apstrādātu pieteikšanās pieprasījumus
@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            
            users_db = User.query.all()
            for user in users_db:
                
                if form_login == user.login and check_str(form_password, user.password):
                    return redirect('/index')
            else:
                error = 'Nepareizs lietotājs vai parole'
                return render_template('login.html', error=error)

            
        else:
            return render_template('login.html', error=error)



# Funkcija, lai parādītu galveno lapu ar kartēm
@app.route('/index')
def index():
    
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)


# Funkcija, lai parādītu konkrētu karti
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Funkcija, lai apstrādātu reģistrācijas pieprasījumus
@app.route('/registration', methods=['GET', 'POST'])
def registration(): 
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        
        hashed_password = hashed_str(password)
        user = User(login=login, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/')
    else:    
        return render_template('registration.html')

# Funkcija, lai parādītu kartes izveides formu
@app.route('/create')
def create():
    return render_template('create_card.html')

@app.route("/create")
def home():
    return render_template('index.html')



# Funkcija, lai apstrādātu kartes izveides pieprasījumus
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        

        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')


# Funkcija, lai apstrādātu kartes dzēšanas pieprasījumus
@app.route("/delete", methods=['POST'])
def delete():

    return redirect('index')

if __name__ == "__main__":
    app.run(debug=True)
