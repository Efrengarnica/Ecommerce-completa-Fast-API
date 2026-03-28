#Ejemplo de como deberá de ser la estructura de manejo de excepciones de mi app.

#Pasos a comprender

""" 
    NOTA: el __init__.py sirve para poder importar modulos y funciones.

    1. Primero defines las clases que heredarán de Exception.

    2. Las clases deben de solo servir de cascaron de información.

    3. En handlers debes de, con la info de arriba, mostrar una respuesta más estructurada que se le dará a
    el cliente.

    4. En handlers, en __init__.py debe de estar presente una función que
    reciba la app y ahí usar add_exception_handler, al final ahí vivirá el manejador de las excepciones.
    
    5.Vincular el manejador con la app, eso es en el main, trayendo la funcion de __init__.py
    y ejecutandola.

    NOTA: Los handlers si son async y la función que los añade como hanlers no
 """

class EjemploException(Exception):

    #Aquí ya estamos armando el cascaron
    def __init__(self, ejemplo_id:int):
        self.ejemplo_id = ejemplo_id
        self.message = f"El ejemplo con ID {ejemplo_id} no se encontró."
        super().__init__(self.message)

    
