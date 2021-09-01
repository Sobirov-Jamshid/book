from .models import Template


keys = Template.keys.all()
messages = Template.messages.all()
smiles = Template.smiles.all()


class Keys():
    LANGUAGE = keys[0]


class Messages():
    WELCOME_USER_MESSAGE = messages[0]
    MESSAGE_HANDLER = messages[1]
    HELP_MESSAGE_HANDLER = messages[2]
    NOT_BOOKS = messages[3]


class Smiles():
    SMILE = smiles[0]
