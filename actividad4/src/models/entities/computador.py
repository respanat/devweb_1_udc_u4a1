from src import db  # Importamos la instancia de SQLAlchemy
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .usuario import Usuario


class Computador(db.Model):
    __tablename__ = 'computadores'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    marca: Mapped[str] = mapped_column(String(100), nullable=False) 
    categoria: Mapped[str] = mapped_column(String(100), nullable=False)
    marca_cpu: Mapped[str] = mapped_column("marcaCpu", String(100))
    velocidad_cpu: Mapped[float] = mapped_column("velocidadCpu", Float)
    tecnologia_ram: Mapped[str] = mapped_column("tecnologiaRam", String(50))
    capacidad_ram: Mapped[int] = mapped_column("capacidadRam", Integer)
    tecnologia_disco: Mapped[str] = mapped_column("tecnologiaDisco", String(50))
    capacidad_disco: Mapped[int] = mapped_column("capacidadDisco", Integer)
    num_puertos_usb: Mapped[int] = mapped_column("numPuertosUSB", Integer)
    num_puertos_hdmi: Mapped[int] = mapped_column("numPuertosHDMI", Integer)
    marca_monitor: Mapped[str] = mapped_column("marcaMonitor", String(100))
    pulgadas: Mapped[float] = mapped_column(Float)
    precio: Mapped[float] = mapped_column(Float)

    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey('usuarios.id'))
    usuario: Mapped['usuario'] = relationship(Usuario, backref='computadores')

    # Constructor
    def __init__(self, marca, categoria, marca_cpu, velocidad_cpu, tecnologia_ram,
                 capacidad_ram, tecnologia_disco, capacidad_disco, num_puertos_usb,
                 num_puertos_hdmi, marca_monitor, pulgadas, precio, usuarios_id=None, usuario=None, id=None):
        
        self.marca = marca
        self.categoria = categoria
        self.marca_cpu = marca_cpu
        self.velocidad_cpu = velocidad_cpu
        self.tecnologia_ram = tecnologia_ram
        self.capacidad_ram = capacidad_ram
        self.tecnologia_disco = tecnologia_disco
        self.capacidad_disco = capacidad_disco
        self.num_puertos_usb = num_puertos_usb
        self.num_puertos_hdmi = num_puertos_hdmi
        self.marca_monitor = marca_monitor
        self.pulgadas = pulgadas
        self.precio = precio
        
        if usuarios_id is not None:
            self.usuarios_id = usuarios_id
        if usuario is not None:
            self.usuario = usuario
        
        if id is not None:
            self.id = id

    def __repr__(self):
        return (f"<Computador(id={self.id}, marca='{self.marca}', "
                f"categoria='{self.categoria}', marca_cpu='{self.marca_cpu}', "
                f"usuario_id={self.usuario_id})>")
