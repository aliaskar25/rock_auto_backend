from django.contrib import admin

from .models import (
    Mark, Year, MarkModel, Complectation, Detail, SubDetail,
)


admin.site.register(Mark)
admin.site.register(Year)
admin.site.register(MarkModel)
admin.site.register(Complectation)
admin.site.register(Detail)
admin.site.register(SubDetail)
