from django.urls import path
from . import views

urlpatterns = [
    path("student-details", views.student_details, name="student-details"),
    path("groups/<int:pk>", views.notes_folder, name="folder-notes"),
    path("groups/<int:group_id>/<int:folder_id>", views.notes, name="notes"),
    path("delete-folder", views.delete_folder, name="delete_folder"),
    path("rename-foler", views.folder_rename, name="rename_folder"),
    path(
        "delete-file/<int:group_id>/<int:folder_id>",
        views.delete_file,
        name="delete_file",
    ),
    path("manage-groups", views.manage_groups, name="showgroup"),
    path("download/<int:file_id>", views.download, name="download"),
    
]
