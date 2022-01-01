from django.contrib import admin

# Register your models here.
from .models import User, Post, Comment
from django.contrib.auth.admin import UserAdmin

# this is how we register our model with different style
@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'id', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('email','id', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {
            "fields": (
                'email',
                'age',
                'password',
                'username',
                'first_name',
                'last_name',
                'image',
                'address',
            ),
        }),
        ('permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ('wide',),
            "fields": (
                'email',
                'age',
                'username',
                'image',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            ),
        }),
    )
    

    ordering = ('email',)

admin.site.register(Post)
admin.site.register(Comment)