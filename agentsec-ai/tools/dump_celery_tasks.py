from backend.workers import celery_app

try:
    tasks = getattr(celery_app, 'tasks', None)
    if tasks is None:
        print('NO_TASKS')
    else:
        print('\n'.join(sorted(tasks.keys())))
except Exception as e:
    print('ERROR', e)
