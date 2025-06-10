from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Text, Sequence, DateTime, SmallInteger,func, Float

from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
Base= declarative_base()



class Telefono(Base):
    __tablename__ = 'telefono'
    id_telefono = Column(Integer, primary_key=True)
    telefono = Column(String(45), nullable=False)
    apoderados = relationship('Apoderado', back_populates='telefono')
    veterinarios = relationship('Veterinario', back_populates='telefono')

    def __repr__(self):
        return f"<Telefono(id_telefono={self.id_telefono}, telefono={self.telefono})>"

    @staticmethod
    def agregar_telefono(session, telefono):
        nuevo_telefono = Telefono(telefono=telefono)
        session.add(nuevo_telefono)
        session.commit()
        print('Teléfono agregado correctamente')
        return nuevo_telefono.id_telefono

    @staticmethod
    def obtener_telefono(session, id_telefono):
        telefono = session.query(Telefono).filter_by(
            id_telefono=id_telefono).first()
        if telefono:
            print(f"Teléfono encontrado: {telefono.telefono}")
            return telefono
        print('Teléfono no encontrado')
        return None

    @staticmethod
    def listar_telefonos(session):
        telefonos = session.query(Telefono).all()
        for telefono in telefonos:
            print(f"ID: {telefono.id_telefono}, Teléfono: {telefono.telefono}")
        return telefonos

    @staticmethod
    def modificar_telefono(session, id_telefono, telefono):
        telefono_obj = session.query(Telefono).filter_by(
            id_telefono=id_telefono).first()
        if telefono_obj:
            telefono_obj.telefono = telefono
            session.commit()
            print('Teléfono actualizado correctamente')
        else:
            print('Teléfono no encontrado')

    @staticmethod
    def eliminar_telefono(session, id_telefono):
        telefono = session.query(Telefono).filter_by(
            id_telefono=id_telefono).first()
        if telefono:
            session.delete(telefono)
            session.commit()
            print('Teléfono eliminado correctamente')
        else:
            print('Teléfono no encontrado')


class Direccion(Base):
    __tablename__ = 'direccion'
    id_direccion = Column(Integer, primary_key=True)
    zona = Column(String(45), nullable=False)
    calle = Column(String(45), nullable=False)
    nro = Column(String(45), nullable=False)
    apoderados = relationship('Apoderado', back_populates='direccion')
    veterinarios = relationship('Veterinario', back_populates='direccion')

    def __repr__(self):
        return f"<Direccion(id_direccion={self.id_direccion}, zona={self.zona}, calle={self.calle}, nro={self.nro})>"

    @staticmethod
    def agregar_direccion(session, zona, calle, nro):
        nueva_direccion = Direccion(zona=zona, calle=calle, nro=nro)
        session.add(nueva_direccion)
        session.commit()
        print('Dirección agregada correctamente')
        return nueva_direccion.id_direccion

    @staticmethod
    def obtener_direccion(session, id_direccion):
        direccion = session.query(Direccion).filter_by(
            id_direccion=id_direccion).first()
        if direccion:
            print(
                f"Dirección encontrada: {direccion.zona}, {direccion.calle}, {direccion.nro}")
            return direccion
        print('Dirección no encontrada')
        return None

    @staticmethod
    def listar_direcciones(session):
        direcciones = session.query(Direccion).all()
        for direccion in direcciones:
            print(
                f"ID: {direccion.id_direccion}, Zona: {direccion.zona}, Calle: {direccion.calle}, Nro: {direccion.nro}")
        return direcciones

    @staticmethod
    def modificar_direccion(session, id_direccion, **kwargs):
        direccion = session.query(Direccion).filter_by(
            id_direccion=id_direccion).first()
        if direccion:
            for key, value in kwargs.items():
                setattr(direccion, key, value)
            session.commit()
            print('Dirección actualizada correctamente')
        else:
            print('Dirección no encontrada')

    @staticmethod
    def eliminar_direccion(session, id_direccion):
        direccion = session.query(Direccion).filter_by(
            id_direccion=id_direccion).first()
        if direccion:
            session.delete(direccion)
            session.commit()
            print('Dirección eliminada correctamente')
        else:
            print('Dirección no encontrada')


class Apoderado(Base):
    __tablename__ = 'apoderado'
    id_apoderado = Column(Integer, primary_key=True)
    ci = Column(String(50), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    id_telefono = Column(Integer, ForeignKey(
        'telefono.id_telefono'), nullable=False)
    id_direccion = Column(Integer, ForeignKey(
        'direccion.id_direccion'), nullable=False)
    telefono = relationship('Telefono', back_populates='apoderados')
    direccion = relationship('Direccion', back_populates='apoderados')
    pacientes = relationship('Paciente', back_populates='apoderado')

    def __repr__(self):
        return f"<Apoderado(id_apoderado={self.id_apoderado}, ci={self.ci}, nombre={self.nombre}, apellido={self.apellido})>"

    @staticmethod
    def agregar_apoderado(session, ci, nombre, apellido, id_telefono, id_direccion):
        nuevo_apoderado = Apoderado(
            ci=ci, nombre=nombre, apellido=apellido, id_telefono=id_telefono, id_direccion=id_direccion)
        session.add(nuevo_apoderado)
        session.commit()
        print('Apoderado agregado correctamente')

    @staticmethod
    def obtener_apoderado(session, id_apoderado):
        apoderado = session.query(Apoderado).filter_by(
            id_apoderado=id_apoderado).first()
        if apoderado:
            print(
                f"Apoderado encontrado: {apoderado.nombre} {apoderado.apellido}, CI: {apoderado.ci}")
            return apoderado
        print('Apoderado no encontrado')
        return None

    @staticmethod
    def listar_apoderados(session):
        apoderados = session.query(Apoderado).all()
        for apoderado in apoderados:
            print(
                f"ID: {apoderado.id_apoderado}, CI: {apoderado.ci}, Nombre: {apoderado.nombre}, Apellido: {apoderado.apellido}")
        return apoderados

    @staticmethod
    def modificar_apoderado(session, id_apoderado, **kwargs):
        apoderado = session.query(Apoderado).filter_by(
            id_apoderado=id_apoderado).first()
        if apoderado:
            for key, value in kwargs.items():
                setattr(apoderado, key, value)
            session.commit()
            print('Apoderado actualizado correctamente')
        else:
            print('Apoderado no encontrado')

    @staticmethod
    def eliminar_apoderado(session, id_apoderado):
        apoderado = session.query(Apoderado).filter_by(
            id_apoderado=id_apoderado).first()
        if apoderado:
            session.delete(apoderado)
            session.commit()
            print('Apoderado eliminado correctamente')
        else:
            print('Apoderado no encontrado')


class DescripcionGeneral(Base):
    __tablename__ = 'descripcion_general'
    id_descripcion_general = Column(Integer, primary_key=True)
    fecha_edicion = Column(Date, nullable=False)
    historial = relationship('Historial', back_populates='descripcion_general')
    padecimientos = relationship(
        'DescripcionGeneralPadecimientos', back_populates='descripcion_general')
    tratamientos = relationship(
        'DescripcionGeneralTratamientos', back_populates='descripcion_general')

    def __repr__(self):
        return f"<DescripcionGeneral(id_descripcion_general={self.id_descripcion_general}, fecha_edicion={self.fecha_edicion})>"

    @staticmethod
    def agregar_descripcion_general(session, fecha_edicion):
        nueva_descripcion = DescripcionGeneral(fecha_edicion=fecha_edicion)
        session.add(nueva_descripcion)
        session.commit()
        print('Descripción general agregada correctamente')
        return nueva_descripcion.id_descripcion_general

    @staticmethod
    def obtener_descripcion_general(session, id_descripcion_general):
        descripcion = session.query(DescripcionGeneral).filter_by(
            id_descripcion_general=id_descripcion_general).first()
        if descripcion:
            print(
                f"Descripción general encontrada: Fecha edición {descripcion.fecha_edicion}")
            return descripcion
        print('Descripción general no encontrada')
        return None

    @staticmethod
    def listar_descripciones_generales(session):
        descripciones = session.query(DescripcionGeneral).all()
        for descripcion in descripciones:
            print(
                f"ID: {descripcion.id_descripcion_general}, Fecha edición: {descripcion.fecha_edicion}")
        return descripciones

    @staticmethod
    def modificar_descripcion_general(session, id_descripcion_general, fecha_edicion):
        descripcion = session.query(DescripcionGeneral).filter_by(
            id_descripcion_general=id_descripcion_general).first()
        if descripcion:
            descripcion.fecha_edicion = fecha_edicion
            session.commit()
            print('Descripción general actualizada correctamente')
        else:
            print('Descripción general no encontrada')

    @staticmethod
    def eliminar_descripcion_general(session, id_descripcion_general):
        descripcion = session.query(DescripcionGeneral).filter_by(
            id_descripcion_general=id_descripcion_general).first()
        if descripcion:
            session.delete(descripcion)
            session.commit()
            print('Descripción general eliminada correctamente')
        else:
            print('Descripción general no encontrada')


class TipoConsulta(Base):
    __tablename__ = 'tipoconsulta'
    id_tipo_consulta = Column(Integer, primary_key=True)
    tipo_consulta = Column(String(50), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    intervenciones = relationship(
        'Intervenciones', back_populates='tipo_consulta')
    vacunaciones = relationship('Vacunacion', back_populates='tipo_consulta')
    derivaciones = relationship('Deriva', back_populates='tipo_consulta')

    def __repr__(self):
        return f"<TipoConsulta(id_tipo_consulta={self.id_tipo_consulta}, tipo_consulta={self.tipo_consulta}, precio={self.precio})>"

    @staticmethod
    def agregar_tipo_consulta(session, tipo_consulta, precio):
        nuevo_tipo = TipoConsulta(tipo_consulta=tipo_consulta, precio=precio)
        session.add(nuevo_tipo)
        session.commit()
        print('Tipo de consulta agregado correctamente')

    @staticmethod
    def obtener_tipo_consulta(session, id_tipo_consulta):
        tipo = session.query(TipoConsulta).filter_by(
            id_tipo_consulta=id_tipo_consulta).first()
        if tipo:
            print(
                f"Tipo de consulta encontrado: {tipo.tipo_consulta}, Precio: {tipo.precio}")
            return tipo
        print('Tipo de consulta no encontrado')
        return None

    @staticmethod
    def listar_tipos_consulta(session):
        tipos = session.query(TipoConsulta).all()
        for tipo in tipos:
            print(
                f"ID: {tipo.id_tipo_consulta}, Tipo: {tipo.tipo_consulta}, Precio: {tipo.precio}")
        return tipos

    @staticmethod
    def modificar_tipo_consulta(session, id_tipo_consulta, **kwargs):
        tipo = session.query(TipoConsulta).filter_by(
            id_tipo_consulta=id_tipo_consulta).first()
        if tipo:
            for key, value in kwargs.items():
                setattr(tipo, key, value)
            session.commit()
            print('Tipo de consulta actualizado correctamente')
        else:
            print('Tipo de consulta no encontrado')

    @staticmethod
    def eliminar_tipo_consulta(session, id_tipo_consulta):
        tipo = session.query(TipoConsulta).filter_by(
            id_tipo_consulta=id_tipo_consulta).first()
        if tipo:
            session.delete(tipo)
            session.commit()
            print('Tipo de consulta eliminado correctamente')
        else:
            print('Tipo de consulta no encontrado')


class Intervenciones(Base):
    __tablename__ = 'intervenciones'
    id_intervencion = Column(Integer, primary_key=True)
    cirugia = Column(String(50), nullable=False)
    fecha_seguimiento = Column(Date, nullable=False)
    complicaciones = Column(Text, nullable=False)
    id_tipo_consulta = Column(Integer, ForeignKey(
        'tipoconsulta.id_tipo_consulta'), nullable=False)
    tipo_consulta = relationship(
        'TipoConsulta', back_populates='intervenciones')

    def __repr__(self):
        return f"<Intervenciones(id_intervencion={self.id_intervencion}, cirugia={self.cirugia})>"

    @staticmethod
    def agregar_intervencion(session, cirugia, fecha_seguimiento, complicaciones, id_tipo_consulta):
        nueva_intervencion = Intervenciones(
            cirugia=cirugia, fecha_seguimiento=fecha_seguimiento, complicaciones=complicaciones, id_tipo_consulta=id_tipo_consulta)
        session.add(nueva_intervencion)
        session.commit()
        print('Intervención agregada correctamente')

    @staticmethod
    def obtener_intervencion(session, id_intervencion):
        intervencion = session.query(Intervenciones).filter_by(
            id_intervencion=id_intervencion).first()
        if intervencion:
            print(
                f"Intervención encontrada: {intervencion.cirugia}, Fecha seguimiento: {intervencion.fecha_seguimiento}")
            return intervencion
        print('Intervención no encontrada')
        return None

    @staticmethod
    def listar_intervenciones(session):
        intervenciones = session.query(Intervenciones).all()
        for intervencion in intervenciones:
            print(
                f"ID: {intervencion.id_intervencion}, Cirugía: {intervencion.cirugia}, Fecha seguimiento: {intervencion.fecha_seguimiento}")
        return intervenciones

    @staticmethod
    def modificar_intervencion(session, id_intervencion, **kwargs):
        intervencion = session.query(Intervenciones).filter_by(
            id_intervencion=id_intervencion).first()
        if intervencion:
            for key, value in kwargs.items():
                setattr(intervencion, key, value)
            session.commit()
            print('Intervención actualizada correctamente')
        else:
            print('Intervención no encontrada')

    @staticmethod
    def eliminar_intervencion(session, id_intervencion):
        intervencion = session.query(Intervenciones).filter_by(
            id_intervencion=id_intervencion).first()
        if intervencion:
            session.delete(intervencion)
            session.commit()
            print('Intervención eliminada correctamente')
        else:
            print('Intervención no encontrada')


class Paciente(Base):
    __tablename__ = 'paciente'
    id_paciente = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    edad = Column(Integer, nullable=False)
    id_apoderado = Column(Integer, ForeignKey(
        'apoderado.id_apoderado'), nullable=False)
    apoderado = relationship('Apoderado', back_populates='pacientes')
    visitas = relationship('Visita', back_populates='paciente')

    def __repr__(self):
        return f"<Paciente(id_paciente={self.id_paciente}, nombre={self.nombre}, especie={self.especie})>"

    @staticmethod
    def agregar_paciente(session, nombre, especie, raza, fecha_nacimiento, edad, id_apoderado):
        nuevo_paciente = Paciente(nombre=nombre, especie=especie, raza=raza,
                                  fecha_nacimiento=fecha_nacimiento, edad=edad, id_apoderado=id_apoderado)
        session.add(nuevo_paciente)
        session.commit()
        print('Paciente agregado correctamente')

    @staticmethod
    def obtener_paciente(session, id_paciente):
        paciente = session.query(Paciente).filter_by(
            id_paciente=id_paciente).first()
        if paciente:
            print(
                f"Paciente encontrado: {paciente.nombre}, Especie: {paciente.especie}, Raza: {paciente.raza}")
            return paciente
        print('Paciente no encontrado')
        return None

    @staticmethod
    def listar_pacientes(session):
        pacientes = session.query(Paciente).all()
        for paciente in pacientes:
            print(
                f"ID: {paciente.id_paciente}, Nombre: {paciente.nombre}, Especie: {paciente.especie}, Raza: {paciente.raza}")
        return pacientes

    @staticmethod
    def modificar_paciente(session, id_paciente, **kwargs):
        paciente = session.query(Paciente).filter_by(
            id_paciente=id_paciente).first()
        if paciente:
            for key, value in kwargs.items():
                setattr(paciente, key, value)
            session.commit()
            print('Paciente actualizado correctamente')
        else:
            print('Paciente no encontrado')

    @staticmethod
    def eliminar_paciente(session, id_paciente):
        paciente = session.query(Paciente).filter_by(
            id_paciente=id_paciente).first()
        if paciente:
            session.delete(paciente)
            session.commit()
            print('Paciente eliminado correctamente')
        else:
            print('Paciente no encontrado')


class Sala(Base):
    __tablename__ = 'sala'
    id_sala = Column(Integer, primary_key=True)
    numero_salas = Column(Integer, nullable=False)
    estado_salas = relationship('EstadoSala', back_populates='sala')
    derivaciones = relationship('Deriva', back_populates='sala')

    def __repr__(self):
        return f"<Sala(id_sala={self.id_sala}, numero_salas={self.numero_salas})>"

    @staticmethod
    def agregar_sala(session, numero_salas):
        nueva_sala = Sala(numero_salas=numero_salas)
        session.add(nueva_sala)
        session.commit()
        print('Sala agregada correctamente')

    @staticmethod
    def obtener_sala(session, id_sala):
        sala = session.query(Sala).filter_by(id_sala=id_sala).first()
        if sala:
            print(f"Sala encontrada: Número de salas {sala.numero_salas}")
            return sala
        print('Sala no encontrada')
        return None

    @staticmethod
    def listar_salas(session):
        salas = session.query(Sala).all()
        for sala in salas:
            print(f"ID: {sala.id_sala}, Número de salas: {sala.numero_salas}")
        return salas

    @staticmethod
    def modificar_sala(session, id_sala, numero_salas):
        sala = session.query(Sala).filter_by(id_sala=id_sala).first()
        if sala:
            sala.numero_salas = numero_salas
            session.commit()
            print('Sala actualizada correctamente')
        else:
            print('Sala no encontrada')

    @staticmethod
    def eliminar_sala(session, id_sala):
        sala = session.query(Sala).filter_by(id_sala=id_sala).first()
        if sala:
            session.delete(sala)
            session.commit()
            print('Sala eliminada correctamente')
        else:
            print('Sala no encontrada')


class Veterinario(Base):
    __tablename__ = 'veterinario'
    id_veterinario = Column(Integer, primary_key=True)
    ci = Column(String(50), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    especialidad = Column(String(100), nullable=False)
    id_telefono = Column(Integer, ForeignKey(
        'telefono.id_telefono'), nullable=False)
    id_direccion = Column(Integer, ForeignKey(
        'direccion.id_direccion'), nullable=False)
    telefono = relationship('Telefono', back_populates='veterinarios')
    direccion = relationship('Direccion', back_populates='veterinarios')
    visitas = relationship('Visita', back_populates='veterinario')

    def __repr__(self):
        return f"<Veterinario(id_veterinario={self.id_veterinario}, ci={self.ci}, nombre={self.nombre})>"

    @staticmethod
    def agregar_veterinario(session, ci, nombre, apellido, especialidad, id_telefono, id_direccion):
        nuevo_veterinario = Veterinario(ci=ci, nombre=nombre, apellido=apellido,
                                        especialidad=especialidad, id_telefono=id_telefono, id_direccion=id_direccion)
        session.add(nuevo_veterinario)
        session.commit()
        print('Veterinario agregado correctamente')

    @staticmethod
    def obtener_veterinario(session, id_veterinario):
        veterinario = session.query(Veterinario).filter_by(
            id_veterinario=id_veterinario).first()
        if veterinario:
            print(
                f"Veterinario encontrado: {veterinario.nombre} {veterinario.apellido}, Especialidad: {veterinario.especialidad}")
            return veterinario
        print('Veterinario no encontrado')
        return None

    @staticmethod
    def listar_veterinarios(session):
        veterinarios = session.query(Veterinario).all()
        for veterinario in veterinarios:
            print(f"ID: {veterinario.id_veterinario}, CI: {veterinario.ci}, Nombre: {veterinario.nombre}, Apellido: {veterinario.apellido}, Especialidad: {veterinario.especialidad}")
        return veterinarios

    @staticmethod
    def modificar_veterinario(session, id_veterinario, **kwargs):
        veterinario = session.query(Veterinario).filter_by(
            id_veterinario=id_veterinario).first()
        if veterinario:
            for key, value in kwargs.items():
                setattr(veterinario, key, value)
            session.commit()
            print('Veterinario actualizado correctamente')
        else:
            print('Veterinario no encontrado')

    @staticmethod
    def eliminar_veterinario(session, id_veterinario):
        veterinario = session.query(Veterinario).filter_by(
            id_veterinario=id_veterinario).first()
        if veterinario:
            session.delete(veterinario)
            session.commit()
            print('Veterinario eliminado correctamente')
        else:
            print('Veterinario no encontrado')


class Historial(Base):
    __tablename__ = 'historial'
    id_historial = Column(Integer, primary_key=True)
    id_descripcion_general = Column(Integer, ForeignKey(
        'descripcion_general.id_descripcion_general'), nullable=False)
    descripcion_general = relationship(
        'DescripcionGeneral', back_populates='historial')
    visitas = relationship('Visita', back_populates='historial')

    def __repr__(self):
        return f"<Historial(id_historial={self.id_historial})>"

    @staticmethod
    def agregar_historial(session, id_descripcion_general):
        nuevo_historial = Historial(
            id_descripcion_general=id_descripcion_general)
        session.add(nuevo_historial)
        session.commit()
        print('Historial agregado correctamente')

    @staticmethod
    def obtener_historial(session, id_historial):
        historial = session.query(Historial).filter_by(
            id_historial=id_historial).first()
        if historial:
            print(
                f"Historial encontrado: ID descripción general {historial.id_descripcion_general}")
            return historial
        print('Historial no encontrado')
        return None

    @staticmethod
    def listar_historiales(session):
        historiales = session.query(Historial).all()
        for historial in historiales:
            print(
                f"ID: {historial.id_historial}, ID descripción general: {historial.id_descripcion_general}")
        return historiales

    @staticmethod
    def modificar_historial(session, id_historial, id_descripcion_general):
        historial = session.query(Historial).filter_by(
            id_historial=id_historial).first()
        if historial:
            historial.id_descripcion_general = id_descripcion_general
            session.commit()
            print('Historial actualizado correctamente')
        else:
            print('Historial no encontrado')

    @staticmethod
    def eliminar_historial(session, id_historial):
        historial = session.query(Historial).filter_by(
            id_historial=id_historial).first()
        if historial:
            session.delete(historial)
            session.commit()
            print('Historial eliminado correctamente')
        else:
            print('Historial no encontrado')


class Visita(Base):
    __tablename__ = 'visita'
    id_visita = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    motivo = Column(String(255), nullable=False)
    id_veterinario = Column(Integer, ForeignKey(
        'veterinario.id_veterinario'), nullable=False)
    id_paciente = Column(Integer, ForeignKey(
        'paciente.id_paciente'), nullable=False)
    id_historial = Column(Integer, ForeignKey(
        'historial.id_historial'), nullable=False)
    veterinario = relationship('Veterinario', back_populates='visitas')
    paciente = relationship('Paciente', back_populates='visitas')
    historial = relationship('Historial', back_populates='visitas')
    tipopagos = relationship('TipoPago', back_populates='visita')
    derivaciones = relationship('Deriva', back_populates='visita')

    def __repr__(self):
        return f"<Visita(id_visita={self.id_visita}, fecha={self.fecha}, motivo={self.motivo})>"

    @staticmethod
    def agregar_visita(session, fecha, motivo, id_veterinario, id_paciente, id_historial):
        nueva_visita = Visita(fecha=fecha, motivo=motivo, id_veterinario=id_veterinario,
                              id_paciente=id_paciente, id_historial=id_historial)
        session.add(nueva_visita)
        session.commit()
        print('Visita agregada correctamente')

    @staticmethod
    def obtener_visita(session, id_visita):
        visita = session.query(Visita).filter_by(id_visita=id_visita).first()
        if visita:
            print(
                f"Visita encontrada: Fecha {visita.fecha}, Motivo: {visita.motivo}")
            return visita
        print('Visita no encontrada')
        return None

    @staticmethod
    def listar_visitas(session):
        visitas = session.query(Visita).all()
        for visita in visitas:
            print(
                f"ID: {visita.id_visita}, Fecha: {visita.fecha}, Motivo: {visita.motivo}")
        return visitas

    @staticmethod
    def modificar_visita(session, id_visita, **kwargs):
        visita = session.query(Visita).filter_by(id_visita=id_visita).first()
        if visita:
            for key, value in kwargs.items():
                setattr(visita, key, value)
            session.commit()
            print('Visita actualizada correctamente')
        else:
            print('Visita no encontrada')

    @staticmethod
    def eliminar_visita(session, id_visita):
        visita = session.query(Visita).filter_by(id_visita=id_visita).first()
        if visita:
            session.delete(visita)
            session.commit()
            print('Visita eliminada correctamente')
        else:
            print('Visita no encontrada')


class TipoPago(Base):
    __tablename__ = 'tipopago'
    id_tipo_pago = Column(Integer, primary_key=True)
    monto = Column(Numeric(10, 2), nullable=False)
    fecha_pago = Column(Date, nullable=False)
    id_visita = Column(Integer, ForeignKey('visita.id_visita'), nullable=False)
    tipo_pago = Column(String(50), nullable=False)
    visita = relationship('Visita', back_populates='tipopagos')

    def __repr__(self):
        return f"<TipoPago(id_tipo_pago={self.id_tipo_pago}, monto={self.monto}, tipo_pago={self.tipo_pago})>"

    @staticmethod
    def agregar_tipo_pago(session, monto, fecha_pago, id_visita, tipo_pago):
        nuevo_pago = TipoPago(monto=monto, fecha_pago=fecha_pago,
                              id_visita=id_visita, tipo_pago=tipo_pago)
        session.add(nuevo_pago)
        session.commit()
        print('Tipo de pago agregado correctamente')

    @staticmethod
    def obtener_tipo_pago(session, id_tipo_pago):
        pago = session.query(TipoPago).filter_by(
            id_tipo_pago=id_tipo_pago).first()
        if pago:
            print(
                f"Tipo de pago encontrado: Monto {pago.monto}, Tipo: {pago.tipo_pago}")
            return pago
        print('Tipo de pago no encontrado')
        return None

    @staticmethod
    def listar_tipos_pago(session):
        pagos = session.query(TipoPago).all()
        for pago in pagos:
            print(
                f"ID: {pago.id_tipo_pago}, Monto: {pago.monto}, Tipo: {pago.tipo_pago}, Fecha: {pago.fecha_pago}")
        return pagos

    @staticmethod
    def modificar_tipo_pago(session, id_tipo_pago, **kwargs):
        pago = session.query(TipoPago).filter_by(
            id_tipo_pago=id_tipo_pago).first()
        if pago:
            for key, value in kwargs.items():
                setattr(pago, key, value)
            session.commit()
            print('Tipo de pago actualizado correctamente')
        else:
            print('Tipo de pago no encontrado')

    @staticmethod
    def eliminar_tipo_pago(session, id_tipo_pago):
        pago = session.query(TipoPago).filter_by(
            id_tipo_pago=id_tipo_pago).first()
        if pago:
            session.delete(pago)
            session.commit()
            print('Tipo de pago eliminado correctamente')
        else:
            print('Tipo de pago no encontrado')


class Vacunacion(Base):
    __tablename__ = 'vacunacion'
    id_vacunacion = Column(Integer, primary_key=True)
    vacuna = Column(String(50), nullable=False)
    dosis = Column(Numeric(10, 2), nullable=False)
    fecha_proxima_vacuna = Column(Date, nullable=False)
    id_tipo_consulta = Column(Integer, ForeignKey(
        'tipoconsulta.id_tipo_consulta'), nullable=False)
    tipo_consulta = relationship('TipoConsulta', back_populates='vacunaciones')

    def __repr__(self):
        return f"<Vacunacion(id_vacunacion={self.id_vacunacion}, vacuna={self.vacuna})>"

    @staticmethod
    def agregar_vacunacion(session, vacuna, dosis, fecha_proxima_vacuna, id_tipo_consulta):
        nueva_vacunacion = Vacunacion(
            vacuna=vacuna, dosis=dosis, fecha_proxima_vacuna=fecha_proxima_vacuna, id_tipo_consulta=id_tipo_consulta)
        session.add(nueva_vacunacion)
        session.commit()
        print('Vacunación agregada correctamente')

    @staticmethod
    def obtener_vacunacion(session, id_vacunacion):
        vacunacion = session.query(Vacunacion).filter_by(
            id_vacunacion=id_vacunacion).first()
        if vacunacion:
            print(
                f"Vacunación encontrada: {vacunacion.vacuna}, Dosis: {vacunacion.dosis}")
            return vacunacion
        print('Vacunación no encontrada')
        return None

    @staticmethod
    def listar_vacunaciones(session):
        vacunaciones = session.query(Vacunacion).all()
        for vacunacion in vacunaciones:
            print(f"ID: {vacunacion.id_vacunacion}, Vacuna: {vacunacion.vacuna}, Dosis: {vacunacion.dosis}, Fecha próxima: {vacunacion.fecha_proxima_vacuna}")
        return vacunaciones

    @staticmethod
    def modificar_vacunacion(session, id_vacunacion, **kwargs):
        vacunacion = session.query(Vacunacion).filter_by(
            id_vacunacion=id_vacunacion).first()
        if vacunacion:
            for key, value in kwargs.items():
                setattr(vacunacion, key, value)
            session.commit()
            print('Vacunación actualizada correctamente')
        else:
            print('Vacunación no encontrada')

    @staticmethod
    def eliminar_vacunacion(session, id_vacunacion):
        vacunacion = session.query(Vacunacion).filter_by(
            id_vacunacion=id_vacunacion).first()
        if vacunacion:
            session.delete(vacunacion)
            session.commit()
            print('Vacunación eliminada correctamente')
        else:
            print('Vacunación no encontrada')


class Deriva(Base):
    __tablename__ = 'deriva'
    id_derivacion = Column(Integer, primary_key=True)
    id_visita = Column(Integer, ForeignKey('visita.id_visita'), nullable=False)
    id_tipo_consulta = Column(Integer, ForeignKey(
        'tipoconsulta.id_tipo_consulta'), nullable=False)
    id_sala = Column(Integer, ForeignKey('sala.id_sala'), nullable=False)
    visita = relationship('Visita', back_populates='derivaciones')
    tipo_consulta = relationship('TipoConsulta', back_populates='derivaciones')
    sala = relationship('Sala', back_populates='derivaciones')

    def __repr__(self):
        return f"<Deriva(id_derivacion={self.id_derivacion})>"

    @staticmethod
    def agregar_derivacion(session, id_visita, id_tipo_consulta, id_sala):
        nueva_derivacion = Deriva(
            id_visita=id_visita, id_tipo_consulta=id_tipo_consulta, id_sala=id_sala)
        session.add(nueva_derivacion)
        session.commit()
        print('Derivación agregada correctamente')

    @staticmethod
    def obtener_derivacion(session, id_derivacion):
        derivacion = session.query(Deriva).filter_by(
            id_derivacion=id_derivacion).first()
        if derivacion:
            print(
                f"Derivación encontrada: Visita ID {derivacion.id_visita}, Tipo consulta ID {derivacion.id_tipo_consulta}, Sala ID {derivacion.id_sala}")
            return derivacion
        print('Derivación no encontrada')
        return None

    @staticmethod
    def listar_derivaciones(session):
        derivaciones = session.query(Deriva).all()
        for derivacion in derivaciones:
            print(f"ID: {derivacion.id_derivacion}, Visita ID: {derivacion.id_visita}, Tipo consulta ID: {derivacion.id_tipo_consulta}, Sala ID: {derivacion.id_sala}")
        return derivaciones

    @staticmethod
    def modificar_derivacion(session, id_derivacion, **kwargs):
        derivacion = session.query(Deriva).filter_by(
            id_derivacion=id_derivacion).first()
        if derivacion:
            for key, value in kwargs.items():
                setattr(derivacion, key, value)
            session.commit()
            print('Derivación actualizada correctamente')
        else:
            print('Derivación no encontrada')

    @staticmethod
    def eliminar_derivacion(session, id_derivacion):
        derivacion = session.query(Deriva).filter_by(
            id_derivacion=id_derivacion).first()
        if derivacion:
            session.delete(derivacion)
            session.commit()
            print('Derivación eliminada correctamente')
        else:
            print('Derivación no encontrada')


class EstadoSala(Base):
    __tablename__ = 'estado_sala'
    id_estado_sala = Column(Integer, primary_key=True)
    estado = Column(String(45), nullable=False)
    id_sala = Column(Integer, ForeignKey('sala.id_sala'), nullable=False)
    sala = relationship('Sala', back_populates='estado_salas')

    def __repr__(self):
        return f"<EstadoSala(id_estado_sala={self.id_estado_sala}, estado={self.estado})>"

    @staticmethod
    def agregar_estado_sala(session, estado, id_sala):
        nuevo_estado = EstadoSala(estado=estado, id_sala=id_sala)
        session.add(nuevo_estado)
        session.commit()
        print('Estado de sala agregado correctamente')

    @staticmethod
    def obtener_estado_sala(session, id_estado_sala):
        estado = session.query(EstadoSala).filter_by(
            id_estado_sala=id_estado_sala).first()
        if estado:
            print(
                f"Estado de sala encontrado: {estado.estado}, Sala ID: {estado.id_sala}")
            return estado
        print('Estado de sala no encontrado')
        return None

    @staticmethod
    def listar_estados_sala(session):
        estados = session.query(EstadoSala).all()
        for estado in estados:
            print(
                f"ID: {estado.id_estado_sala}, Estado: {estado.estado}, Sala ID: {estado.id_sala}")
        return estados

    @staticmethod
    def modificar_estado_sala(session, id_estado_sala, **kwargs):
        estado = session.query(EstadoSala).filter_by(
            id_estado_sala=id_estado_sala).first()
        if estado:
            for key, value in kwargs.items():
                setattr(estado, key, value)
            session.commit()
            print('Estado de sala actualizado correctamente')
        else:
            print('Estado de sala no encontrado')

    @staticmethod
    def eliminar_estado_sala(session, id_estado_sala):
        estado = session.query(EstadoSala).filter_by(
            id_estado_sala=id_estado_sala).first()
        if estado:
            session.delete(estado)
            session.commit()
            print('Estado de sala eliminado correctamente')
        else:
            print('Estado de sala no encontrado')


class Vacunas(Base):
    __tablename__ = 'vacunas'
    id_vacunas = Column(Integer, primary_key=True)
    vacuna = Column(String(45), nullable=False)
    fecha_vacuna = Column(Date, nullable=False)
    descripcion_genera_vacunas = relationship(
        'DescripcionGeneraVacunas', back_populates='vacunas')

    def __repr__(self):
        return f"<Vacunas(id_vacunas={self.id_vacunas}, vacuna={self.vacuna})>"

    @staticmethod
    def agregar_vacuna(session, vacuna, fecha_vacuna):
        nueva_vacuna = Vacunas(vacuna=vacuna, fecha_vacuna=fecha_vacuna)
        session.add(nueva_vacuna)
        session.commit()
        print('Vacuna agregada correctamente')

    @staticmethod
    def obtener_vacuna(session, id_vacunas):
        vacuna = session.query(Vacunas).filter_by(
            id_vacunas=id_vacunas).first()
        if vacuna:
            print(
                f"Vacuna encontrada: {vacuna.vacuna}, Fecha: {vacuna.fecha_vacuna}")
            return vacuna
        print('Vacuna no encontrada')
        return None

    @staticmethod
    def listar_vacunas(session):
        vacunas = session.query(Vacunas).all()
        for vacuna in vacunas:
            print(
                f"ID: {vacuna.id_vacunas}, Vacuna: {vacuna.vacuna}, Fecha: {vacuna.fecha_vacuna}")
        return vacunas

    @staticmethod
    def modificar_vacuna(session, id_vacunas, **kwargs):
        vacuna = session.query(Vacunas).filter_by(
            id_vacunas=id_vacunas).first()
        if vacuna:
            for key, value in kwargs.items():
                setattr(vacuna, key, value)
            session.commit()
            print('Vacuna actualizada correctamente')
        else:
            print('Vacuna no encontrada')

    @staticmethod
    def eliminar_vacuna(session, id_vacunas):
        vacuna = session.query(Vacunas).filter_by(
            id_vacunas=id_vacunas).first()
        if vacuna:
            session.delete(vacuna)
            session.commit()
            print('Vacuna eliminada correctamente')
        else:
            print('Vacuna no encontrada')


class EstadoPadecimientos(Base):
    __tablename__ = 'estado_padecimientos'
    id_estado_padecimientos = Column(Integer, primary_key=True)
    estado_padecimientos = Column(String(45), nullable=False)
    padecimientos = relationship(
        'Padecimientos', back_populates='estado_padecimientos')

    def __repr__(self):
        return f"<EstadoPadecimientos(id_estado_padecimientos={self.id_estado_padecimientos}, estado_padecimientos={self.estado_padecimientos})>"

    @staticmethod
    def agregar_estado_padecimiento(session, estado_padecimientos):
        nuevo_estado = EstadoPadecimientos(
            estado_padecimientos=estado_padecimientos)
        session.add(nuevo_estado)
        session.commit()
        print('Estado de padecimiento agregado correctamente')

    @staticmethod
    def obtener_estado_padecimiento(session, id_estado_padecimientos):
        estado = session.query(EstadoPadecimientos).filter_by(
            id_estado_padecimientos=id_estado_padecimientos).first()
        if estado:
            print(
                f"Estado de padecimiento encontrado: {estado.estado_padecimientos}")
            return estado
        print('Estado de padecimiento no encontrado')
        return None

    @staticmethod
    def listar_estados_padecimientos(session):
        estados = session.query(EstadoPadecimientos).all()
        for estado in estados:
            print(
                f"ID: {estado.id_estado_padecimientos}, Estado: {estado.estado_padecimientos}")
        return estados

    @staticmethod
    def modificar_estado_padecimiento(session, id_estado_padecimientos, estado_padecimientos):
        estado = session.query(EstadoPadecimientos).filter_by(
            id_estado_padecimientos=id_estado_padecimientos).first()
        if estado:
            estado.estado_padecimientos = estado_padecimientos
            session.commit()
            print('Estado de padecimiento actualizado correctamente')
        else:
            print('Estado de padecimiento no encontrado')

    @staticmethod
    def eliminar_estado_padecimiento(session, id_estado_padecimientos):
        estado = session.query(EstadoPadecimientos).filter_by(
            id_estado_padecimientos=id_estado_padecimientos).first()
        if estado:
            session.delete(estado)
            session.commit()
            print('Estado de padecimiento eliminado correctamente')
        else:
            print('Estado de padecimiento no encontrado')


class Padecimientos(Base):
    __tablename__ = 'padecimientos'
    id_padecimientos = Column(Integer, primary_key=True)
    padecimientos = Column(String(45), nullable=False)
    id_estado_padecimientos = Column(Integer, ForeignKey(
        'estado_padecimientos.id_estado_padecimientos'), nullable=False)
    estado_padecimientos = relationship(
        'EstadoPadecimientos', back_populates='padecimientos')
    descripcion_general_padecimientos = relationship(
        'DescripcionGeneralPadecimientos', back_populates='padecimientos')

    def __repr__(self):
        return f"<Padecimientos(id_padecimientos={self.id_padecimientos}, padecimientos={self.padecimientos})>"

    @staticmethod
    def agregar_padecimiento(session, padecimientos, id_estado_padecimientos):
        nuevo_padecimiento = Padecimientos(
            padecimientos=padecimientos, id_estado_padecimientos=id_estado_padecimientos)
        session.add(nuevo_padecimiento)
        session.commit()
        print('Padecimiento agregado correctamente')

    @staticmethod
    def obtener_padecimiento(session, id_padecimientos):
        padecimiento = session.query(Padecimientos).filter_by(
            id_padecimientos=id_padecimientos).first()
        if padecimiento:
            print(f"Padecimiento encontrado: {padecimiento.padecimientos}")
            return padecimiento
        print('Padecimiento no encontrado')
        return None

    @staticmethod
    def listar_padecimientos(session):
        padecimientos = session.query(Padecimientos).all()
        for padecimiento in padecimientos:
            print(f"ID: {padecimiento.id_padecimientos}, Padecimiento: {padecimiento.padecimientos}, Estado ID: {padecimiento.id_estado_padecimientos}")
        return padecimientos

    @staticmethod
    def modificar_padecimiento(session, id_padecimientos, **kwargs):
        padecimiento = session.query(Padecimientos).filter_by(
            id_padecimientos=id_padecimientos).first()
        if padecimiento:
            for key, value in kwargs.items():
                setattr(padecimiento, key, value)
            session.commit()
            print('Padecimiento actualizado correctamente')
        else:
            print('Padecimiento no encontrado')

    @staticmethod
    def eliminar_padecimiento(session, id_padecimientos):
        padecimiento = session.query(Padecimientos).filter_by(
            id_padecimientos=id_padecimientos).first()
        if padecimiento:
            session.delete(padecimiento)
            session.commit()
            print('Padecimiento eliminado correctamente')
        else:
            print('Padecimiento no encontrado')


class Tratamientos(Base):
    __tablename__ = 'tratamientos'
    id_tratamientos = Column(Integer, primary_key=True)
    tratamiento = Column(String(45), nullable=False)
    descripcion_general_tratamientos = relationship(
        'DescripcionGeneralTratamientos', back_populates='tratamientos')

    def __repr__(self):
        return f"<Tratamientos(id_tratamientos={self.id_tratamientos}, tratamiento={self.tratamiento})>"

    @staticmethod
    def agregar_tratamiento(session, tratamiento):
        nuevo_tratamiento = Tratamientos(tratamiento=tratamiento)
        session.add(nuevo_tratamiento)
        session.commit()
        print('Tratamiento agregado correctamente')

    @staticmethod
    def obtener_tratamiento(session, id_tratamientos):
        tratamiento = session.query(Tratamientos).filter_by(
            id_tratamientos=id_tratamientos).first()
        if tratamiento:
            print(f"Tratamiento encontrado: {tratamiento.tratamiento}")
            return tratamiento
        print('Tratamiento no encontrado')
        return None

    @staticmethod
    def listar_tratamientos(session):
        tratamientos = session.query(Tratamientos).all()
        for tratamiento in tratamientos:
            print(
                f"ID: {tratamiento.id_tratamientos}, Tratamiento: {tratamiento.tratamiento}")
        return tratamientos

    @staticmethod
    def modificar_tratamiento(session, id_tratamientos, tratamiento):
        tratamiento_obj = session.query(Tratamientos).filter_by(
            id_tratamientos=id_tratamientos).first()
        if tratamiento_obj:
            tratamiento_obj.tratamiento = tratamiento
            session.commit()
            print('Tratamiento actualizado correctamente')
        else:
            print('Tratamiento no encontrado')

    @staticmethod
    def eliminar_tratamiento(session, id_tratamientos):
        tratamiento = session.query(Tratamientos).filter_by(
            id_tratamientos=id_tratamientos).first()
        if tratamiento:
            session.delete(tratamiento)
            session.commit()
            print('Tratamiento eliminado correctamente')
        else:
            print('Tratamiento no encontrado')


class DescripcionGeneraVacunas(Base):
    __tablename__ = 'descripcion_genera_vacunas'
    id_descripcion_genera_vacunas = Column(Integer, primary_key=True)
    id_historial = Column(Integer, ForeignKey(
        'descripcion_general.id_descripcion_general'), nullable=False)
    id_vacunas = Column(Integer, ForeignKey(
        'vacunas.id_vacunas'), nullable=False)
    historial = relationship('DescripcionGeneral',
                             backref='descripcion_genera_vacunas')
    vacunas = relationship(
        'Vacunas', back_populates='descripcion_genera_vacunas')

    def __repr__(self):
        return f"<DescripcionGeneraVacunas(id_descripcion_genera_vacunas={self.id_descripcion_genera_vacunas})>"

    @staticmethod
    def agregar_descripcion_vacuna(session, id_historial, id_vacunas):
        nueva_descripcion = DescripcionGeneraVacunas(
            id_historial=id_historial, id_vacunas=id_vacunas)
        session.add(nueva_descripcion)
        session.commit()
        print('Descripción de vacuna agregada correctamente')

    @staticmethod
    def obtener_descripcion_vacuna(session, id_descripcion_genera_vacunas):
        descripcion = session.query(DescripcionGeneraVacunas).filter_by(
            id_descripcion_genera_vacunas=id_descripcion_genera_vacunas).first()
        if descripcion:
            print(
                f"Descripción de vacuna encontrada: Historial ID {descripcion.id_historial}, Vacuna ID {descripcion.id_vacunas}")
            return descripcion
        print('Descripción de vacuna no encontrada')
        return None

    @staticmethod
    def listar_descripciones_vacunas(session):
        descripciones = session.query(DescripcionGeneraVacunas).all()
        for descripcion in descripciones:
            print(f"ID: {descripcion.id_descripcion_genera_vacunas}, Historial ID: {descripcion.id_historial}, Vacuna ID: {descripcion.id_vacunas}")
        return descripciones

    @staticmethod
    def modificar_descripcion_vacuna(session, id_descripcion_genera_vacunas, **kwargs):
        descripcion = session.query(DescripcionGeneraVacunas).filter_by(
            id_descripcion_genera_vacunas=id_descripcion_genera_vacunas).first()
        if descripcion:
            for key, value in kwargs.items():
                setattr(descripcion, key, value)
            session.commit()
            print('Descripción de vacuna actualizada correctamente')
        else:
            print('Descripción de vacuna no encontrada')

    @staticmethod
    def eliminar_descripcion_vacuna(session, id_descripcion_genera_vacunas):
        descripcion = session.query(DescripcionGeneraVacunas).filter_by(
            id_descripcion_genera_vacunas=id_descripcion_genera_vacunas).first()
        if descripcion:
            session.delete(descripcion)
            session.commit()
            print('Descripción de vacuna eliminada correctamente')
        else:
            print('Descripción de vacuna no encontrada')


class DescripcionGeneralPadecimientos(Base):
    __tablename__ = 'descripcion_general_padecimientos'
    id_descripcion_general_padecimientos = Column(Integer, primary_key=True)
    id_descripcion_general = Column(Integer, ForeignKey(
        'descripcion_general.id_descripcion_general'), nullable=False)
    id_padecimientos = Column(Integer, ForeignKey(
        'padecimientos.id_padecimientos'), nullable=False)
    descripcion_general = relationship(
        'DescripcionGeneral', back_populates='padecimientos')
    padecimientos = relationship(
        'Padecimientos', back_populates='descripcion_general_padecimientos')

    def __repr__(self):
        return f"<DescripcionGeneralPadecimientos(id_descripcion_general_padecimientos={self.id_descripcion_general_padecimientos})>"

    @staticmethod
    def agregar_descripcion_padecimiento(session, id_descripcion_general, id_padecimientos):
        nueva_descripcion = DescripcionGeneralPadecimientos(
            id_descripcion_general=id_descripcion_general, id_padecimientos=id_padecimientos)
        session.add(nueva_descripcion)
        session.commit()
        print('Descripción de padecimiento agregada correctamente')

    @staticmethod
    def obtener_descripcion_padecimiento(session, id_descripcion_general_padecimientos):
        descripcion = session.query(DescripcionGeneralPadecimientos).filter_by(
            id_descripcion_general_padecimientos=id_descripcion_general_padecimientos).first()
        if descripcion:
            print(
                f"Descripción de padecimiento encontrada: Descripción general ID {descripcion.id_descripcion_general}, Padecimiento ID {descripcion.id_padecimientos}")
            return descripcion
        print('Descripción de padecimiento no encontrada')
        return None

    @staticmethod
    def listar_descripciones_padecimientos(session):
        descripciones = session.query(DescripcionGeneralPadecimientos).all()
        for descripcion in descripciones:
            print(f"ID: {descripcion.id_descripcion_general_padecimientos}, Descripción general ID: {descripcion.id_descripcion_general}, Padecimiento ID: {descripcion.id_padecimientos}")
        return descripciones

    @staticmethod
    def modificar_descripcion_padecimiento(session, id_descripcion_general_padecimientos, **kwargs):
        descripcion = session.query(DescripcionGeneralPadecimientos).filter_by(
            id_descripcion_general_padecimientos=id_descripcion_general_padecimientos).first()
        if descripcion:
            for key, value in kwargs.items():
                setattr(descripcion, key, value)
            session.commit()
            print('Descripción de padecimiento actualizada correctamente')
        else:
            print('Descripción de padecimiento no encontrada')

    @staticmethod
    def eliminar_descripcion_padecimiento(session, id_descripcion_general_padecimientos):
        descripcion = session.query(DescripcionGeneralPadecimientos).filter_by(
            id_descripcion_general_padecimientos=id_descripcion_general_padecimientos).first()
        if descripcion:
            session.delete(descripcion)
            session.commit()
            print('Descripción de padecimiento eliminada correctamente')
        else:
            print('Descripción de padecimiento no encontrada')


class DescripcionGeneralTratamientos(Base):
    __tablename__ = 'descripcion_general_tratamientos'
    id_descripcion_general_tratamientos = Column(Integer, primary_key=True)
    id_descripcion_general = Column(Integer, ForeignKey(
        'descripcion_general.id_descripcion_general'), nullable=False)
    id_tratamientos = Column(Integer, ForeignKey(
        'tratamientos.id_tratamientos'), nullable=False)
    descripcion_general = relationship(
        'DescripcionGeneral', back_populates='tratamientos')
    tratamientos = relationship(
        'Tratamientos', back_populates='descripcion_general_tratamientos')

    def __repr__(self):
        return f"<DescripcionGeneralTratamientos(id_descripcion_general_tratamientos={self.id_descripcion_general_tratamientos})>"

    @staticmethod
    def agregar_descripcion_tratamiento(session, id_descripcion_general, id_tratamientos):
        nueva_descripcion = DescripcionGeneralTratamientos(
            id_descripcion_general=id_descripcion_general, id_tratamientos=id_tratamientos)
        session.add(nueva_descripcion)
        session.commit()
        print('Descripción de tratamiento agregada correctamente')

    @staticmethod
    def obtener_descripcion_tratamiento(session, id_descripcion_general_tratamientos):
        descripcion = session.query(DescripcionGeneralTratamientos).filter_by(
            id_descripcion_general_tratamientos=id_descripcion_general_tratamientos).first()
        if descripcion:
            print(
                f"Descripción de tratamiento encontrada: Descripción general ID {descripcion.id_descripcion_general}, Tratamiento ID {descripcion.id_tratamientos}")
            return descripcion
        print('Descripción de tratamiento no encontrada')
        return None

    @staticmethod
    def listar_descripciones_tratamientos(session):
        descripciones = session.query(DescripcionGeneralTratamientos).all()
        for descripcion in descripciones:
            print(f"ID: {descripcion.id_descripcion_general_tratamientos}, Descripción general ID: {descripcion.id_descripcion_general}, Tratamiento ID: {descripcion.id_tratamientos}")
        return descripciones

    @staticmethod
    def modificar_descripcion_tratamiento(session, id_descripcion_general_tratamientos, **kwargs):
        descripcion = session.query(DescripcionGeneralTratamientos).filter_by(
            id_descripcion_general_tratamientos=id_descripcion_general_tratamientos).first()
        if descripcion:
            for key, value in kwargs.items():
                setattr(descripcion, key, value)
            session.commit()
            print('Descripción de tratamiento actualizada correctamente')
        else:
            print('Descripción de tratamiento no encontrada')

    @staticmethod
    def eliminar_descripcion_tratamiento(session, id_descripcion_general_tratamientos):
        descripcion = session.query(DescripcionGeneralTratamientos).filter_by(
            id_descripcion_general_tratamientos=id_descripcion_general_tratamientos).first()
        if descripcion:
            session.delete(descripcion)
            session.commit()
            print('Descripción de tratamiento eliminada correctamente')
        else:
            print('Descripción de tratamiento no encontrada')

from flask_login import UserMixin

class Usuario(Base, UserMixin):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
