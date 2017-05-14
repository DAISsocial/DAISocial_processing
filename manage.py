from manager import Manager

from server import ProcessingServer

manager = Manager()


@manager.command
def runserver():
    ProcessingServer().run()
