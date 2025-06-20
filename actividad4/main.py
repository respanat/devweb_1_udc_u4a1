from src import create_app # Importa la función de creación de la aplicación

app = create_app() # Crea la instancia de la aplicación Flask

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=8082) # modo debug
