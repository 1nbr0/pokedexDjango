from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PokeTeam
from .models import User
from .models import UserInfo

# Register your models here.
class UserInfoInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name_plural = 'UserInfo'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInfoInline,)

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(PokeTeam)
