from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_rJivSW4LqY2g@ep-long-resonance-ahgm6az8-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'
app.config['SECRET_KEY'] = 'odev_gizli_anahtar_final' 
db = SQLAlchemy(app)

# ==========================================
# MODELLER
# ==========================================
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(200))
    icon = db.Column(db.String(20))
    professionals = db.relationship('Professional', backref='service', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='service', lazy=True, cascade="all, delete-orphan")

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50))
    professional_name = db.Column(db.String(50))
    customer_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    date = db.Column(db.String(50))
    status = db.Column(db.String(20), default='Bekliyor')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    customer_name = db.Column(db.String(100))

# ==========================================
# İLK KURULUM (Tekrarlamayı Önleyen Kontrollü Yükleme)
# ==========================================
def verileri_yukle():
    
    if Service.query.first():
        return

    data = [
        {"name": "Berber", "desc": "Saç-sakal kesimi.", "icon": "✂️", "u": ["Ahmet Y.", "Mehmet D.", "Can T."]},
        {"name": "Psikolog", "desc": "Terapi desteği.", "icon": "🧠", "u": ["Dr. Zeynep K.", "Psk. Elif Ş."]},
        {"name": "Köpek Gezdirme", "desc": "Güvenli yürüyüş.", "icon": "🐕", "u": ["Ozan T.", "Deniz M."]},
        {"name": "Yaşam Koçu", "desc": "Hedef planlama.", "icon": "🚀", "u": ["Serdar A.", "Meltem K."]},
        {"name": "Spor Eğitmeni", "desc": "Antrenman desteği.", "icon": "💪", "u": ["Barış G.", "Sinan H."]},
        {"name": "Sosyal Medya", "desc": "Hesap yönetimi.", "icon": "📱", "u": ["İrem K.", "Damla Y."]}
    ]
    for item in data:
        srv = Service(name=item["name"], desc=item["desc"], icon=item["icon"])
        db.session.add(srv)
        db.session.commit() # Önce hizmeti kaydet ki ID oluşsun
        for isim in item["u"]:
            db.session.add(Professional(name=isim, service_id=srv.id))
        db.session.commit()

# ==========================================
# ROTALAR
# ==========================================
@app.route('/')
def index():
    services = Service.query.all()
    last_reviews = Review.query.order_by(Review.id.desc()).limit(6).all()
    return render_template('index6.html', services=services, reviews=last_reviews)

@app.route('/service/<int:id>')
def detail(id):
    service = Service.query.get_or_404(id)
    professionals = Professional.query.filter_by(service_id=id).all()
    return render_template('detay7.html', service=service, professionals=professionals)

@app.route('/book/<int:service_id>', methods=['POST'])
def book(service_id):
    service = Service.query.get_or_404(service_id)
    prof = Professional.query.get(request.form.get('professional_id'))
    full_date = f"{request.form.get('randevu_tarihi')} - {request.form.get('randevu_saati')}"
    
    # ÇAKIŞMA KONTROLÜ
    if Appointment.query.filter_by(professional_name=prof.name, date=full_date).first():
        flash(f"Üzgünüz, {prof.name} için bu saat dolu!", "error")
        return redirect(url_for('detail', id=service_id))
    
    new_app = Appointment(service_name=service.name, professional_name=prof.name, 
                          customer_name=request.form.get('customer_name'), 
                          phone=request.form.get('phone'), date=full_date)
    db.session.add(new_app)
    db.session.commit()
    return render_template('basarili.html')

@app.route('/randevularim', methods=['GET', 'POST'])
def my_appointments():
    apps = None
    aranan = ""
    if request.method == 'POST':
        aranan = request.form.get('isim_sorgu')
        apps = Appointment.query.filter(Appointment.customer_name.contains(aranan)).all()
    return render_template('randevularim6.html', appointments=apps, aranan=aranan)

@app.route('/add_review', methods=['POST'])
def add_review():
    s_name = request.form.get('service_name')
    service = Service.query.filter_by(name=s_name).first()
    if service:
        new_rev = Review(service_id=service.id, rating=int(request.form.get('rating')), 
                         comment=request.form.get('comment'), customer_name=request.form.get('customer_name'))
        db.session.add(new_rev)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_appointment(id):
    ap = Appointment.query.get(id)
    if ap:
        db.session.delete(ap)
        db.session.commit()
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard', sayfa='randevular'))
    return redirect(url_for('my_appointments'))

@app.route('/admin/delete_review/<int:id>')
def delete_review(id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    rev = Review.query.get(id)
    if rev:
        db.session.delete(rev)
        db.session.commit()
    return redirect(url_for('admin_dashboard', sayfa='yorumlar'))

# --- ADMIN PANELİ ---
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST' and request.form.get('password') == 'melikeyagmur8585':
        session['admin_logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    aktif_sayfa = request.args.get('sayfa', 'ozet')
    all_apps = Appointment.query.order_by(Appointment.id.desc()).all()
    all_services = Service.query.all()
    all_reviews = Review.query.all()
    
    # GRAFİK VERİLERİ 
    labels = [s.name for s in all_services]
    data = [Appointment.query.filter_by(service_name=s.name).count() for s in all_services]
    
    return render_template('admin_panel.html', aktif_sayfa=aktif_sayfa, appointments=all_apps, 
                           services=all_services, reviews=all_reviews, count=len(all_apps), 
                           earnings=len(all_apps)*350, labels=labels, data=data)

@app.route('/admin/toggle_status/<int:id>')
def toggle_status(id):
    ap = Appointment.query.get(id)
    if ap:
        ap.status = "Tamamlandı" if ap.status == "Bekliyor" else "Bekliyor"
        db.session.commit()
    return redirect(url_for('admin_dashboard', sayfa='randevular'))

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        verileri_yukle()
    app.run(debug=True)
