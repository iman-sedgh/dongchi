from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User



UserAdmin.fieldsets +=  (
        ('Financial System', {'fields': ('is_financialstaff',)}),
        ('Custom Profile', {'fields': ('avatar',)}),
    )

UserAdmin.list_display =  ('username', 
                             'is_staff', 
                            'is_financialstaff' , 
                            'phone_number',
                        )


admin.site.register(User, UserAdmin)
