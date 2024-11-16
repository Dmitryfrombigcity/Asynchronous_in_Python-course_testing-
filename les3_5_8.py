# import asyncio
# import contextvars
#
# ctx_msg = contextvars.ContextVar('Сообщение')
# ctx_fileno = contextvars.ContextVar('файловый дескриптор')
# ctx_permission = contextvars.ContextVar('право доступа')
#
# ctx_msg.set('deleted ID 4660')
# ctx_fileno.set('11128')
# ctx_permission.set('DOMAIN\\admin')

async def print_msg() -> str:
    return (f'{ctx.get(ctx_msg, 'failure')}, '
            f'fileno={ctx.get(ctx_fileno, 'failure')}, '
            f'{ctx.get(ctx_permission, 'guest')}')


# if __name__ == '__main__':
#     ctx = contextvars.copy_context()
#     print(asyncio.run(ctx.run(print_msg)))
