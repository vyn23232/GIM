from django.contrib import admin
from .models import User, Dashboard, Membership, Booking, Class, Attendance,Trainer,Exercise

admin.site.register(User)
admin.site.register(Dashboard)
admin.site.register(Membership)
admin.site.register(Booking)
admin.site.register(Class)
admin.site.register(Attendance)
admin.site.register(Trainer)
admin.site.register(Exercise)
