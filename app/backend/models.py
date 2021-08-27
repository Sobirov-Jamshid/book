from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            type=BotUser.Type.USER,
        )


class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            type=BotUser.Type.ADMIN,
        )

class BotUser(models.Model):
    class Lang(models.TextChoices):
        UZ = 'uz'
        RU = 'ru'
        EN = 'en'

    class Type(models.TextChoices):
        USER = 'user'
        ADMIN = 'admin'
       
    objects = models.Manager()
    users = UserManager()
    admins = AdminManager()
    

    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.USER
    )
    chat_id = models.IntegerField(unique=True)
    full_name = models.CharField(max_length=255, verbose_name="To'liq ismi")
    lang = models.CharField(
        max_length=10,
        choices=Lang.choices,
        default=Lang.UZ
    )
    bot_state = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = verbose_name + 'lar'

    def __str__(self):
        return self.full_name


class Books(models.Model):
    name = models.CharField(max_length=255)
    file_id = models.CharField(max_length=255)
    count = models.IntegerField()

    def __str__(self):
        return self.name
    




class KeyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Key')


class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Message')


class SmileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Smile')



class Template(models.Model):
    class Type(models.TextChoices):
        KEY = 'Key'
        MESSAGE = 'Message'
        SMILE = 'Smile'

    templates = models.Manager()
    keys = KeyManager()
    messages = MessageManager()
    smiles = SmileManager()

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Type.choices)
    body_uz = models.TextField()
    body_ru = models.TextField()
    body_en = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)

        keys = Template.keys.all()
        messages = Template.messages.all()
        smiles = Template.smiles.all()
        with open('backend/templates.py', 'w') as file:
            file.write('from .models import Template\n\n')
            file.write('\n')
            file.write('keys = Template.keys.all()\n')
            file.write('messages = Template.messages.all()\n')
            file.write('smiles = Template.smiles.all()\n\n')
            file.write('\n')
            file.write('class Keys():\n')
            for index, key in enumerate(keys):
                file.write(f'    {key.title} = keys[{index}]\n')

            file.write('\n\n')
            file.write('class Messages():\n')
            for index, message in enumerate(messages):
                file.write(f'    {message.title} = messages[{index}]\n')

            file.write('\n\n')
            file.write('class Smiles():\n')
            for index, smile in enumerate(smiles):
                file.write(f'    {smile.title} = smiles[{index}]\n')

        return result

    @property
    def text(self):
        return self.body_uz

    def get(self, lang):
        return getattr(self, f'body_{lang}')

    def getall(self):
        return (self.body_uz, self.body_ru, self.body_en)

    def format(self, **kwargs):
        return self.body_uz.format(**kwargs)

    def __format__(self, format_spec):
        return format(self.body_uz, format_spec)

    def __str__(self):
        return self.title

