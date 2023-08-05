# __init__.py
__name__ = 'casadata'
__all__ = [ 'datapath' ]

import os as os

datapath=(os.path.join(os.path.dirname(os.path.abspath(__file__)),'__data__'))
