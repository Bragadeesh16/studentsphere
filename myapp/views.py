from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from .forms import *
from django.forms import *
from .decorators import authenticate_staff,authenticate_users
from account.models import CustomUser
from Adminuser.models import ClassGroup
from django.contrib import messages


def home(request):
    permission = False
    if request.user.groups.filter(name="staff").exists():
        permission = True
    return render(request, "home.html", {"permission": permission})


@authenticate_users
def groups_list(request):
    group_names = None
    if request.method == 'POST':
        group_names = request.POST.get("search-element")
        if group_names:
            group_names = ClassGroup.objects.filter(name__icontains=group_names)
            if not group_names.exists():
                messages.error(
                request, f"There are no group  '{group_names}'"
            )
    
    return render(
        request,
        "GroupList.html",
        {
            'groups':group_names,
        },
    )


def groupmembers():
    student_list = CustomUser.objects.all()
    new_student = []
    for student in student_list:
        if (
            not student.groups.filter(name="Cse II")
            and not student.groups.filter(name="Cse III")
            and not student.groups.filter(name="Cse IV")
        ):
            new_student.append(student)
    return new_student


