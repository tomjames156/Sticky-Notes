from django.urls import path, include
from .views import *

app_name = 'notes'

urlpatterns = [
    path('', home, name="home"),
    path('search/', search_notes, name="search"),
    path('tinymce/', include('tinymce.urls')),
    path('change_display/<int:display_mode_index>/', change_display_mode, name="change_display"),
    path('notes/<int:pk>/', note_view , name='note'),
    path('update/<int:pk>/', update, name='update'),
    path('delete/<int:pk>/', delete_note, name='delete'),
    path('notes/new/<str:colour_theme>/', new_note, name='new_note'),
    path('notes/<int:pk>/add_image/', add_image, name="add_image"),
    path('notes/<int:pk>/<str:colour>/', change_colour, name='colour'),
    path('notes/<int:pk>/images/<int:image_index>/', view_image, name='view_image'),
    path('notes/<int:pk>/images/<int:image_index>/delete/<int:image_pk>/', delete_img, name="delete_img"),
    path('notes/<int:pk>/images/<int:image_index>/delete_img_from_gal/<int:image_pk>/', delete_img_from_gal, name="delete_img_from_gal"),
    path('notes/<int:pk>/images/<int:image_index>/describe/<int:image_pk>/', describe, name="describe")
]
