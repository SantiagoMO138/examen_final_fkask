@app.route('/add/mensaje', methods=['POST'])
def crear_mensaje():
    with Session() as db_session:
        data = request.json
        try:
            nuevo_mensaje = Mensaje(
                nombre=data.get('nombre'),
                telefono=data.get('telefono'),
                correo=data.get('correo'),
                razon=data.get('razon'),
                detalle=data.get('detalle')
            )
            db_session.add(nuevo_mensaje)
            db_session.commit()
            return jsonify({"mensaje": "Mensaje agregado correctamente"}), 201
        except Exception as e:
            db_session.rollback()
            return jsonify({"error": str(e)}), 400