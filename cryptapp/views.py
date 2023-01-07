
from encodings import utf_8
from importlib.resources import path
from pyexpat import model
from random import choice
from statistics import mode
from unicodedata import name
from attr import fields
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from itsdangerous import base64_encode, encoding
from numpy import size
from rsa import decrypt
from .models import Compressed, Files, Encryption, Decryption, Decompressed
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.conf import settings
from django.core.files.storage import default_storage
import os
from cryptography.fernet import Fernet
import zlib, sys, shutil, gzip
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
# Create your views here.

class Index(CreateView):
    model = Files
    fields = ["file", "name"]

    # This method decrypt the file with the private key that is passed in
    def decryption(self, keys, content):
        try:
            f = Fernet(keys)
            a = f.decrypt(content).decode('ascii')
        except:
            return False
        return a
        
    def encryption(self, content):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(bytes(str(content), encoding='utf-8'))
        return cipher_text, key
        
    def post(self, request):
        m_file = request.FILES['file']
        content = m_file.read()
        f_type = m_file.content_type
        name = request.POST.get('name')
        cho = request.POST.get('choices')
        if f_type not in ['text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            messages.info(request, "Not supported file format")
        else:
            if cho == "Decryption":

                if f_type not in ['text/plain']:
                    return  render(request,'cryptapp/error.html',{'err': "Sorry this Decryption method does not work on the kind of file you chose. Please select the decrypt and decompression method"})
                else:
                    dkey = request.POST.get('dkey')
                    f = Decryption()
                    f.name = name
                    m_file.truncate(0)
                    m_file.seek(0)
                    decrypted = self.decryption(dkey, content)
                    # if decrypted != False:
                    m_file.write(bytes(decrypted, encoding="utf-8"))
                    f.file = m_file
                    f.save()
                    s = Decryption.objects.all()
                    # else:
                    #     return  render(request,'cryptapp/error.html',{'err': "Invalid Decryption key, check key and try again"})

            elif cho == "Encryption":
                if f_type not in ['text/plain']:
                    return  render(request,'cryptapp/error.html',{'err': "Sorry this encryption method does not work on the kind of file you chose, try (.txt) files or select the encrypt and compression method"})
                else:
                    f = Encryption()
                    f.name = name
                    m_file.truncate(0)
                    m_file.seek(0)
                    encrypted, keys = self.encryption(content)
                    m_file.write(encrypted)
                    f.file = m_file
                    f.key = keys.decode('utf-8')
                    f.save()
                    s = Encryption.objects.all()

            elif cho == "Encrypt and Compression":
                f = Compressed()
                try:
                    compressed_data = zlib.compress(content, zlib.Z_BEST_COMPRESSION)
                    f.name = name
                    m_file.truncate(0)
                    m_file.seek(0)
                    m_file.write(compressed_data)
                    f.file = m_file
                    f.save()
                except:
                    return render(request,'cryptapp/error.html',{'err': "The file could not be compressed. Try again"})
                s = Compressed.objects.all()

            elif cho == "Decrypt and Decompression":
                f = Decompressed()
                decompressed_data = zlib.decompress(content)
                f.name = name
                m_file.truncate(0)
                m_file.seek(0)
                m_file.write(decompressed_data)
                f.file = m_file
                f.save()
                s = Decompressed.objects.all()
            return render(request,'cryptapp/download.html',{'file': s})
        return redirect('index')
    
class UsersForm(View):
    form_class = UserForm
    template_name = "cryptapp/users_form.html"
    
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Account Created Successfully")
                return redirect('index')
        else:
            messages.info(request, "Please check your details")
        return render(request, self.template_name)

def loginPage(request):
    template_name = "cryptapp/login.html"
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Incorrect Login details, check your password and username correctly")
    return render(request,template_name)

def log_out(request):
    logout(request)
    return redirect("login")

def about(request):
    return render(request, "cryptapp/about.html")