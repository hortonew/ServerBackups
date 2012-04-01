import sys, os, bottle

os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))

import bottleapp

application = bottle.default_app()
