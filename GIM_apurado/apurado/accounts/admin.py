from django.contrib import admin
from .models import User, Dashboard, Membership, Booking, Class, Attendance

admin.site.register(User)
admin.site.register(Dashboard)
admin.site.register(Membership)
admin.site.register(Booking)
admin.site.register(Class)
admin.site.register(Attendance)
