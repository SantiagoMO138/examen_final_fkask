from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import sessionmaker
from models.base import engine
from models.model import Usuario, Paciente
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key_fallback")

# Crear fábrica de sesiones SQLAlchemy
Session = sessionmaker(bind=engine)

# Setup de LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

@login_manager.user_loader
def load_user(user_id):
    with Session() as db_session:
        return db_session.get(Usuario, int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    with Session() as db_session:
        if request.method == 'POST':
            action = request.form['action']
            if action == 'login':
                username = request.form['username']
                password = request.form['password']
                user = db_session.query(Usuario).filter(
                    Usuario.username == username).first()
                if user and user.check_password(password):
                    login_user(user)
                    flash('Sesión iniciada exitosamente', 'success')
                    return redirect(url_for('home'))  # Changed from 'dashboard' to 'home'
                else:
                    flash('Usuario o contraseña incorrectos', 'danger')
                    return redirect(url_for('auth'))
        return render_template('auth.html', is_admin=current_user.role == 'admin' if current_user.is_authenticated else False)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    with Session() as db_session:
        if request.method == 'POST':
            action = request.form['action']
            if action == 'register':
                if current_user.role != 'admin':
                    flash(
                        'Solo los administradores pueden registrar nuevos usuarios', 'danger')
                    return redirect(url_for('dashboard'))
                username = request.form['username']
                password = request.form['password']
                role = request.form.get('role', 'user')
                if db_session.query(Usuario).filter(Usuario.username == username).first():
                    flash('El usuario ya existe', 'danger')
                else:
                    new_user = Usuario(
                        username=username,
                        password=generate_password_hash(password),
                        role=role
                    )
                    db_session.add(new_user)
                    db_session.commit()
                    flash('Usuario creado exitosamente', 'success')
                return redirect(url_for('dashboard'))
        return render_template('dashboard.html', username=current_user.username, is_admin=current_user.role == 'admin')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))

@app.route('/api/pacientes')
def api_pacientes():
    with Session() as db_session:
        pacientes = db_session.query(Paciente).all()
        pacientes_list = []
        for paciente in pacientes:
            pacientes_list.append({
                "id": paciente.id_paciente,
                "nombre": paciente.nombre,
                "especie": paciente.especie,
                "raza": paciente.raza,
                "fecha_nacimiento": paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
                "edad": paciente.edad,
                "id_apoderado": paciente.id_apoderado
            })
        return jsonify(pacientes_list)

@app.route('/api/filtros', methods=['GET'])
def obtener_filtros():
    with Session() as db_session:
        especie = request.args.getlist('especie')
        raza = request.args.getlist('raza')
        query = db_session.query(Paciente)
        if especie:
            query = query.filter(Paciente.especie.in_(especie))
        if raza:
            query = query.filter(Paciente.raza.in_(raza))
        data = query.all()
        especies = sorted({p.especie for p in data if p.especie})
        razas = sorted({p.raza for p in data if p.raza})
        return jsonify({
            'especies': especies,
            'razas': razas
        })

@app.route('/listpacientes')
@login_required
def listpacientes():
    if current_user.role != 'admin':
        flash('Solo los administradores pueden acceder a esta página', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('crud/list_pacientes.html')

@app.route('/api/list_pacientes')
@login_required
def list_pacientes():
    if current_user.role != 'admin':
        return jsonify({"error": "Solo los administradores pueden acceder a esta API"}), 403
    with Session() as db_session:
        data = db_session.query(Paciente).all()
        pacientes = []
        for paciente in data:
            pacientes.append({
                "id": paciente.id_paciente,
                "nombre": paciente.nombre,
                "especie": paciente.especie,
                "raza": paciente.raza,
                "fecha_nacimiento": paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
                "edad": paciente.edad,
                "id_apoderado": paciente.id_apoderado
            })
        return jsonify(pacientes)

@app.route('/api/opciones', methods=['GET'])
def obtener_opciones():
    with Session() as db_session:
        especies = db_session.query(Paciente.especie).distinct().all()
        razas = db_session.query(Paciente.raza).distinct().all()
        apoderados = db_session.query(Paciente.id_apoderado).distinct().all()
        return jsonify({
            "especies": sorted([e[0] for e in especies if e[0]]),
            "razas": sorted([r[0] for r in razas if r[0]]),
            "apoderados": sorted([a[0] for a in apoderados if a[0]])
        })

@app.route('/add/pacientes', methods=['POST'])
@login_required
def crear_paciente():
    if current_user.role != 'admin':
        return jsonify({"error": "Solo los administradores pueden realizar esta acción"}), 403
    with Session() as db_session:
        data = request.json
        try:
            nuevo = Paciente(
                nombre=data.get('nombre'),
                especie=data.get('especie'),
                raza=data.get('raza'),
                fecha_nacimiento=data.get('fecha_nacimiento'),
                edad=int(data.get('edad')),
                id_apoderado=int(data.get('id_apoderado'))
            )
            db_session.add(nuevo)
            db_session.commit()
            return jsonify({"mensaje": "Paciente agregado correctamente"})
        except Exception as e:
            db_session.rollback()
            return jsonify({"error": str(e)}), 400

@app.route('/del/pacientes/<int:id>', methods=['DELETE'])
@login_required
def eliminar_paciente(id):
    if current_user.role != 'admin':
        return jsonify({"error": "Solo los administradores pueden realizar esta acción"}), 403
    with Session() as db_session:
        paciente = db_session.get(Paciente, id)
        if paciente:
            db_session.delete(paciente)
            db_session.commit()
            return jsonify({"mensaje": "Paciente eliminado correctamente"})
        return jsonify({"error": "Paciente no encontrado"}), 404

@app.route('/upd/pacientes/<int:id>', methods=['PUT'])
@login_required
def actualizar_paciente(id):
    if current_user.role != 'admin':
        return jsonify({"error": "Solo los administradores pueden realizar esta acción"}), 403
    with Session() as db_session:
        paciente = db_session.get(Paciente, id)
        if not paciente:
            return jsonify({"error": "Paciente no encontrado"}), 404
        data = request.json
        try:
            paciente.nombre = data.get("nombre")
            paciente.especie = data.get("especie")
            paciente.raza = data.get("raza")
            paciente.fecha_nacimiento = data.get("fecha_nacimiento")
            paciente.edad = int(data.get("edad")) if data.get("edad") else None
            paciente.id_apoderado = int(data.get("id_apoderado")) if data.get("id_apoderado") else None
            db_session.commit()
            return jsonify({"mensaje": "Paciente actualizado correctamente"})
        except Exception as e:
            db_session.rollback()
            return jsonify({"error": str(e)}), 400

@app.teardown_appcontext
def shutdown_session(exception=None):
    pass

if __name__ == '__main__':
    app.run(debug=True)