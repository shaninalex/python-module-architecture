class CommandBus:

    def __init__(self):
        self._handlers = {}

    def register(self, command_type, handler):
        self._handlers[command_type] = handler

    async def execute(self, command):
        handler = self._handlers[type(command)]
        return await handler(command)
