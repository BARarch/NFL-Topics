from django.contrib import admin
from sheetoutput.models import CredetialsModel
from sheetoutput.models import FlowModel

# Register your models here.

class CredetialsModelAdmin(admin.ModelAdmin):
	pass
admin.site.register(CredetialsModel, CredetialsModelAdmin)

class FlowModelAdmin(admin.ModelAdmin):
	pass
admin.site.register(FlowModel, FlowModelAdmin)

