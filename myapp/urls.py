from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from django.urls import reverse_lazy
urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name = 'signup'),
    path('signin',views.signin,name = 'signin'),
    path('signout',views.signout,name = 'signout'),
    path('profile',views.profile, name = 'profile'),
    path('student-details',views.student_details, name ='student-details'),
    path('groups',views.groups_list,name='group-list'),
    path('groups/<int:pk>',views.notes_folder,name='folder-notes'),
    path('groups/<int:group_id>/<int:folder_id>',views.notes,name = 'notes'),
    path('delete-folder',views.delete_folder,name='delete_folder'),
    path('rename-foler',views.folder_rename,name = 'rename_folder'),
    path('delete-file/<int:group_id>/<int:folder_id>',views.delete_file, name = 'delete_file'),
    # path('addusers',views.adduser,name = 'adduser'),
    # path('chatbot',views.chatbot,name='chatbot')
    path('manage-groups',views.manage_groups,name= 'showgroup'),
    path('cse-second-year',views.Cse_second,name = 'cse_second'),
    path('cse-second-year/remove meember',views.cse_two_remove_member,name = 'cse_second_remove_memeber'),
    path('cse-third',views.Cse_third,name = 'cse_third'),
    path('cse-third-year/remove meember',views.cse_three_remove_member,name = 'cse_three_remove_memeber'),
    path('cse-fourth-year',views.Cse_four,name = 'cse_fourth'),
    path('cse-fourth-year/remove member',views.cse_fourth_remove_member,name = 'cse_four_remove_member'),
    path('download/<int:file_id>', views.download, name='download'),
    path('resetpassword/', views.CustomPasswordResetView.as_view(), name='resetPassword'),
    path('resetpassworddone/', PasswordResetDoneView.as_view(
        template_name = 'password_reset_done.html'
    ), name='resetPasswordDone'),
    path('resetpasswordconfirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name = 'password_reset_confirm.html',
        success_url = reverse_lazy('password_reset_complete')
    ), name = 'password_reset_confirm'),
    path('resetpasswordcomplete/', PasswordResetCompleteView.as_view(
        template_name = 'password_reset_complete.html'
    ), name='password_reset_complete')
    
]