from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import os
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import Group
from django.forms import *
from myapp.decorators import authenticate_staff,authenticate_users
from django.conf import settings
from django.http import HttpResponse, Http404
from account.models import CustomUser,profiles
from .models import *


def CreateDynamicGroup(request):
    pass

# get groups dymaically 
@authenticate_staff
def student_details(request):
    group_two = "Cse II"
    group_three = "Cse III"
    group_four = "Cse IV"

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
    
@authenticate_staff
def manage_groups(request):
    group_list = Group.objects.all()
    return render(request, "manage_groups.html", {"group_list": group_list})


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