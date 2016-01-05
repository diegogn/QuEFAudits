class InstanceCreationErrorTag(BaseException):
    def __init__(self, args):
        self.args = {args}
        self.message = args