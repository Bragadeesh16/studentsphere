from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from .forms import *
from django.contrib.auth.models import Group
from django.forms import *
from .decorators import authenticate_staff,authenticate_users
from django.urls import reverse
from account.models import CustomUser,profiles


def home(request):
    permission = False
    if request.user.groups.filter(name="staff").exists():
        permission = True
    return render(request, "home.html", {"permission": permission})


@authenticate_users
def groups_list(request):
    perm = False
    cse_two = False
    cse_three = False
    cse_four = False
    if request.user.groups.filter(name="staff").exists():
        perm = True
    if request.user.groups.filter(name="Cse II").exists():
        cse_two = True
    if request.user.groups.filter(name="Cse III").exists():
        cse_three = True
    if request.user.groups.filter(name="Cse IV").exists():
        cse_four = True

    return render(
        request,
        "student_groups.html",
        {
            "permission": perm,
            "cse_two": cse_two,
            "cse_three": cse_three,
            "cse_four": cse_four,
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


@authenticate_staff
def Cse_second(request):
    def remove_members_list():
        student_list = CustomUser.objects.all()
        new_student = []
        for student in student_list:
            if student.groups.filter(name="Cse II"):
                new_student.append(student)
        return new_student

    if request.method == "POST":
        selected_students = request.POST.getlist("std")
        student_group = Group.objects.get(name="Cse II")
        for student_name in selected_students:
            user = CustomUser.objects.get(email=student_name)
            user.groups.add(student_group)
        return HttpResponseRedirect(reverse("cse_second"))

    return render(
        request,
        "Csetwo.html",
        {"members_list": groupmembers(), "remove_memeber_list": remove_members_list()},
    )


@authenticate_staff
def cse_two_remove_member(request):
    if request.method == "POST":
        remove_student_names = request.POST.getlist("remove_std")
        student_group = Group.objects.get(name="Cse II")
        for student_name in remove_student_names:
            user = CustomUser.objects.get(email=student_name)
            user.groups.remove(student_group)
        return HttpResponseRedirect(reverse("cse_second"))


@authenticate_staff
def Cse_third(request):
    groupmembers()

    def remove_members_list():
        student_list = CustomUser.objects.all()
        new_student = []
        for student in student_list:
            if student.groups.filter(name="Cse III"):
                new_student.append(student)
        return new_student

    if request.method == "POST":
        selected_students = request.POST.getlist("std")
        student_group = Group.objects.get(name="Cse III")
        for student_name in selected_students:
            user = CustomUser.objects.get(email=student_name)
            user.groups.add(student_group)
        return HttpResponseRedirect(reverse("cse_third"))

    return render(
        request,
        "Csethree.html",
        {"members_list": groupmembers(), "remove_memeber_list": remove_members_list()},
    )


@authenticate_staff
def cse_three_remove_member(request):
    if request.method == "POST":
        remove_student_names = request.POST.getlist("remove_std")
        student_group = Group.objects.get(name="Cse III")
        for student_name in remove_student_names:
            user = CustomUser.objects.get(email=student_name)
            user.groups.remove(student_group)
        return HttpResponseRedirect(reverse("cse_third"))


@authenticate_staff
def Cse_four(request):
    groupmembers()

    def remove_members_list():
        student_list = CustomUser.objects.all()
        new_student = []
        for student in student_list:
            if student.groups.filter(name="Cse IV"):
                new_student.append(student)
        return new_student

    if request.method == "POST":
        selected_students = request.POST.getlist("std")
        student_group = Group.objects.get(name="Cse IV")
        for student_name in selected_students:
            user = CustomUser.objects.get(email=student_name)
            user.groups.add(student_group)
        return HttpResponseRedirect(reverse("cse_fourth"))

    return render(
        request,
        "Csefour.html",
        {"members_list": groupmembers(), "remove_memeber_list": remove_members_list()},
    )


@authenticate_staff
def cse_fourth_remove_member(request):
    if request.method == "POST":
        remove_student_names = request.POST.getlist("remove_std")
        student_group = Group.objects.get(name="Cse IV")
        for student_name in remove_student_names:
            user = CustomUser.objects.get(email=student_name)
            user.groups.remove(student_group)

        return HttpResponseRedirect(reverse("cse_fourth"))
