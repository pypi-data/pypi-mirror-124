'''
All custom exceptions raised in the project.
'''


class InvalidWidgetDefinition(Exception):
    def __init__(self, widget_type):
        self.widget_type = widget_type


class InvalidLayoutError(Exception):
    pass


class InvalidCallbackDefinition(Exception):
    def __init__(self, msg: str):
        self.msg = msg
