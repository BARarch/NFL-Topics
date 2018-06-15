from django.contrib import admin
from parsebot.models import Article

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
	pass
admin.site.register(Article, ArticleAdmin)

