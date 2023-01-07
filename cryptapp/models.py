from pyexpat import model
from django.db import models

# Create your models here.

class Encryption(models.Model):
    file = models.FileField(upload_to="encrypted")
    name = models.CharField(max_length=255, default="defualt")
    key = models.CharField(max_length=255, default='1234')

    def __str__(self):
        return self.name

class Decryption(models.Model):
    file = models.FileField(upload_to="decryted")
    name = models.CharField(max_length=255, default="defualt")

    def __str__(self):
        return self.name

class Compressed(models.Model):
    file = models.FileField(upload_to="compressed")
    name = models.CharField(max_length=255, default="defualt")

    def __str__(self):
        return self.name

class Decompressed(models.Model):
    file = models.FileField(upload_to="decompressed")
    name = models.CharField(max_length=255, default="defualt")

    def __str__(self):
        return self.name


class Files(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=255, default="defualt")
# class Users(models.Model):
