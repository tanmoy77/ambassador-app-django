from django.contrib import admin

from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','first_name', 'last_name')
    list_display_links = ('id','email', )
    ordering = ['id']
    list_filter = ('email',)
    search_fields = ('email',)

admin.site.register(User, UserAdmin)
