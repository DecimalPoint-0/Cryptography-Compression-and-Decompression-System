from http.cookiejar import Cookie
from django.contrib import admin
from .models import Files, Encryption, Decryption, Compressed, Decompressed
# Register your models here.

admin.site.register(Files)
admin.site.register(Encryption)
admin.site.register(Decryption)
admin.site.register(Compressed)
admin.site.register(Decompressed)