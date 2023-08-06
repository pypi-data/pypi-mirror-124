import uuid

from jinja2.ext import Extension


class UUIDGenExtension(Extension):

    def parse(self, parser):
        pass

    def __init__(self, environment):
        super(UUIDGenExtension, self).__init__(environment)

        def uuidgen() -> str:
            return str(uuid.uuid4())

        environment.globals.update(uuidgen=uuidgen)


VTB_EXTENSIONS = [
    UUIDGenExtension
]
