from core.command_bus import CommandBus
from core.event_bus import EventBus


class Application:
    def __init__(self, commands: CommandBus, events: EventBus):
        self.commands = commands
        self.events = events

    async def execute(self, command):
        return await self.commands.execute(command)

    async def publish(self, event):
        return await self.events.publish(event)
