class NotAuthorization(Exception):
    def __init__(self):
        self.mensaje = f"Las claves son incorrectas"
        super().__init__(self.mensaje)