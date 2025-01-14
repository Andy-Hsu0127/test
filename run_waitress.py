from waitress import serve # type: ignore
from quotation_project.wsgi import application

if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=2000)
