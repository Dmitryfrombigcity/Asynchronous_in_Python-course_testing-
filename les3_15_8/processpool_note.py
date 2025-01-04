# Переписывая lock внутри блока with,
# при выходе мы всё-равно снимем блокировку с первоначального

import multiprocessing

lock = multiprocessing.Lock()
nlock = multiprocessing.RLock()

with lock:
    print(f'lock= {lock} {id(lock)}')
    a = lock
    lock = nlock
    print(f'lock= {lock} {id(lock)}')
    with lock:
        print(f'lock= {lock} {id(lock)}')
print(f'lock= {lock} {id(lock)}')
lock = a
print(f'lock= {lock} {id(lock)}')


# lock= <Lock(owner=MainProcess)> 139748132327104
# lock= <RLock(None, 0)> 139748130784032
# lock= <RLock(MainProcess, 1)> 139748130784032
# lock= <RLock(None, 0)> 139748130784032
# lock= <Lock(owner=None)> 139748132327104


