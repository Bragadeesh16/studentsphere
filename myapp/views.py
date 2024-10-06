from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
import openai, os
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.forms import *
from .decorators import authenticate_staff
from .decorators import authenticate_users
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.views import LoginView, PasswordResetView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ValidationError

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

load_dotenv()
api_key = os.getenv("OPENAI_KEY", None)


def home(request):
    permission = False
    if request.user.groups.filter(name="staff").exists():
        permission = True
    return render(request, "home.html", {"permission": permission})


def signup(request):
    form = signup_from()
    if request.method == "POST":
        form = signup_from(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, "your are signed in successfully")
            return redirect("home")
    else:
        form = signup_from()

    return render(
        request,
        "register.html",
        {"form": form},
    )


def signin(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = form.data["email"]
        password = form.data["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "your are logged in successfully")
            return redirect("home")
        else:
            form.add_error(None, _("invalid credentials"))
            # return redirect('signin')
    print(form.non_field_errors())
    return render(request, "login.html", {"form": form})


def signout(request):
    logout(request)
    messages.success(request, "you have been logged out")
    return redirect("home")


@authenticate_users
def profile(request):
    try:
        user_profile = profiles.objects.get(profile_user=request.user)
    except profiles.DoesNotExist:
        user_profile = None

    if request.method == "POST":
        form = profile_form(request.POST, instance=user_profile)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile_user, instance.Name = request.user, request.user.username
            instance.save()
            return redirect("profile")
    else:
        form = profile_form(instance=user_profile)

        return render(
            request,
            "profile.html",
            {
                "form": form,
            },
        )


@authenticate_staff
def student_details(request):
    group_two = "Cse II"
    group_three = "Cse III"
    group_four = "Cse IV"
    perm = False
    if request.user.groups.filter(name="staff").exists():
        perm = True

    def members_details(group_name):
        student_list = CustomUser.objects.filter(groups__name=group_name)
        profile_objects = []
        for student in student_list:
            profile = profiles.objects.filter(profile_user=student)
            profile_objects.append(profile)
        return profile_objects

    return render(
        request,
        "student_details.html",
        {
            "cse_two_details": members_details(group_two),
            "cse_three_details": members_details(group_three),
            "cse_four_details": members_details(group_four),
            "permission": perm,
        },
    )


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


@authenticate_users
def notes_folder(request, pk):
    group_name = Group.objects.get(pk=pk)
    permission = False
    if request.user.groups.filter(name="staff").exists():
        permission = True
    if request.method == "POST":
        form = uploding_folder(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.folder_name = Group.objects.get(name=group_name)
            instance.save()
        else:
            print("Your form is not valid")

    if group_name:
        folders_list = Group.objects.get(name=group_name)
        linked_folders = folders.objects.filter(folder_name=folders_list)
    else:
        linked_folders = []

    form = uploding_folder()

    return render(
        request,
        "notes_folder.html",
        {
            "form": form,
            "group_name": group_name,
            "folder_name": linked_folders,
            "pk": pk,
            "permission": permission,
        },
    )


@authenticate_users
def notes(request, group_id, folder_id):
    form = uploding_documents()
    group = Group.objects.get(pk=group_id)
    folder = folders.objects.get(pk=folder_id)
    permission = False

    if request.user.groups.filter(name="staff").exists():
        permission = True

    if request.method == "POST":
        form = uploding_documents(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.file_from = folder
            instance.save()
            messages.success(request, "Your file is uploaded successfully")
            return redirect("notes", group_id, folder_id)
    try:
        files_list = file_uplode.objects.filter(file_from=folder)
    except folders.DoesNotExist:
        raise Http404("Folder does not exist")
    except file_uplode.DoesNotExist:
        files_list = []

    return render(
        request,
        "notes.html",
        {
            "notes": form,
            "file_list": files_list,
            "permission": permission,
            "group_id": group_id,
            "folder_id": folder_id,
        },
    )


def delete_folder(request):
    if request.method == "POST":
        folder_id, pk = request.POST.get("delete_folder_name").split()
        folder_name = folders.objects.get(id=folder_id)
        folder_name.delete()
        return redirect("folder-notes", pk)


def delete_file(request, group_id, folder_id):
    print(group_id)
    if request.method == "POST":
        file_id = request.POST.get("file_id")
        print(file_id)
        file = file_uplode.objects.get(id=file_id)
        file.delete()
        return redirect("notes", group_id, folder_id)


def folder_rename(request):
    if request.method == "POST":
        file_id, pk = request.POST.get("folder_id").split()
        rename = request.POST.get("rename")
        folder = folders.objects.get(id=file_id)
        folder.name = rename
        folder.save()
        return redirect("folder-notes", pk)


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


@authenticate_staff
def manage_groups(request):
    group_list = Group.objects.all()
    return render(request, "manage_groups.html", {"group_list": group_list})


# def chatbot(request):
#     response = None
#     if request.method == 'POST':
#         user_input = request.POST.get('user_input')
#         api_key = os.getenv('OPENAI_KEY', None)

#         if api_key:
#             openai.api_key = api_key
#             prompt = user_input
#             response = openai.Completion.create(
#                 engine='gpt-3.5-turbo-0613',
#                 prompt=prompt,
#                 max_tokens=256,
#                 temperature=0.5,
#             )
#             if response and response.choices:
#                 response = response.choices[0].text.strip()

#     return render(request, 'gpt.html', {'response': response})
# def adduser(request):
#    if (request.user.groups.filter(name='staff').exists() or request.user.is_superuser):
#         student_list = User.objects.all()
#         new_student = []
#         for student in student_list:
#             if (not student.groups.filter(name = 'student') and not student.is_superuser
#                 and not student.groups.filter(name = 'staff')):
#                 new_student.append(student)

#         if request.method == 'POST':
#             add_student_name = request.POST['std']
#             add_users = User.objects.get(username=add_student_name)
#             add_users  = User.objects.get(id = add_users.id)
#             student_group = Group.objects.get(name = 'student')
#             add_users.groups.add(student_group)

#         return render(request,'manage_groups.html' ,{'student_list':new_student})
#     else:
#         return HttpResponse("you are not allowed")


def download(request, file_id):
    try:
        file = file_uplode.objects.get(pk=file_id)
        path = file.notes
        file_path = os.path.join(settings.MEDIA_ROOT, str(path))

        print("File Path:", file_path)  # Add this line for debugging

        if os.path.exists(file_path):
            with open(file_path, "rb") as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/vnd.ms-excel"
                )
                response["Content-Disposition"] = (
                    "inline; filename=" + os.path.basename(file_path)
                )
                return response
        else:
            print("File does not exist")  # Add this line for debugging
            raise Http404("File not found")
    except file_uplode.DoesNotExist:
        raise Http404("File does not exist")
    except Exception as e:
        # Log the exception for further investigation
        print(f"An error occurred: {str(e)}")
        # You may want to log more detailed information about the error here
        raise Http404("An error occurred while processing the request")


class CustomPasswordResetView(PasswordResetView):
    template_name = "password_reset.html"
    success_url = reverse_lazy("resetPasswordDone")
