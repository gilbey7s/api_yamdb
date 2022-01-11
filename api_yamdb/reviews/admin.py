from django.contrib import admin
<<<<<<< HEAD

from .models import Title, Genre, Category, GenreTitle

admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(GenreTitle)
=======
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
    
>>>>>>> feature/users
