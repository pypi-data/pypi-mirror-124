from kigo.etl.runtime.process import start
from kigo.etl.runtime.storage import get_objects

start('examples')

print(get_objects())
