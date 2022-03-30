from werkzeug.serving import run_simple
# from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from val3dity       import app as val3dity_app
from prepair        import app as prepair_app
from schemacitygml  import app as schemacitygml_app
from welcome        import app as welcome_app

application = DispatcherMiddleware( 
    welcome_app, {
    '/val3dity':        val3dity_app,
    '/schemacitygml':   schemacitygml_app,
    '/prepair':         prepair_app
    }
)

if __name__ == '__main__':
    run_simple('localhost', 5000, application, use_debugger=True, use_reloader=True)


