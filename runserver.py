# see http://flask.pocoo.org/docs/patterns/appdispatch/

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from val3dity import app as val3dity_app
from frontend import app as frontend_app

application = DispatcherMiddleware( frontend_app, {
    '/val3dity':     val3dity_app
})

run_simple('localhost', 5000, application, use_reloader=True)


