class UsuarioNoEncontrado(Exception):
    def __init__(self):
        self.mensaje = f"Usuario no encontrado en la Base de Datos."
        super().__init__(self.mensaje)
