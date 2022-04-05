from django.contrib import admin

from .models import User, Posts, Following, Likez

# Register your models here.

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Following)
admin.site.register(Likez)