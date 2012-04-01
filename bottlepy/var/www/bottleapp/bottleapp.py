from bottle import route, run

@route('/')
def index():
	return 'INDEX FOR BOTTLEAPP - Web1'

@route('/hello/:name')
def hello(name='World'):
    return '<b>Hello %s!</b>' % name

