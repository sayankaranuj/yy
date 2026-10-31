import inspect
import backend.core.eventbus as eb
print('MODULE:', eb.__file__)
print(inspect.getsource(eb.EventBus))
