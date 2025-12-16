from django.shortcuts import render
from django.shortcuts import get_object_or_404


# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Role
from .models import FormRequest, FormApproval
from .serializers import FormSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_form(request):
    data = request.data
    form = FormRequest.objects.create(
        title=data["title"],
        description=data["description"],
        created_by=request.user
    )
    return Response({"message": "Form created", "id": form.id})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_form(request, form_id):
    user = request.user
    form = FormRequest.objects.get(id=form_id)

    user_level = user.role.level

    # Check correct level
    if form.current_level != user_level:
        return Response({"error": "You cannot approve this level"}, status=403)

    # Save approval
    FormApproval.objects.create(
        form=form,
        approved_by=user,
        level=user_level
    )

    max_level = Role.objects.order_by("-level").first().level

    if user_level == max_level:
        form.is_approved = True
    else:
        form.current_level = user_level + 1

    form.save()
    return Response({"message": "Approved!"})




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_approved_forms(request):
    forms = FormRequest.objects.filter(
        created_by=request.user,
        is_approved=True
    ).only("id", "title")

    data = [
        {
            "id": f.id,
            "title": f.title
        }
        for f in forms
    ]

    return Response(data)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_pending_forms(request):
    forms = FormRequest.objects.filter(
        created_by=request.user,
        is_approved=False
    ).only("id", "title", "current_level")

    data = [
        {
            "id": f.id,
            "title": f.title,
            "current_level": f.current_level
        }
        for f in forms
    ]

    return Response(data)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def form_details(request, form_id):

    user = request.user

    if user.role and user.role.level > 1:
        form = get_object_or_404(FormRequest, id=form_id)
    else:
        form = get_object_or_404(
            FormRequest,
            id=form_id,
            created_by=user
        )

    data = {
        "id": form.id,
        "title": form.title,
        "description": form.description,
        "is_approved": form.is_approved,
        "current_level": form.current_level,
        "status": (
            "Approved"
            if form.is_approved
            else f"Pending (Level {form.current_level})"
        ),
        "created_at": form.created_at
    }

    return Response(data)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_approved_forms(request):
    if request.user.role.level <= 1:
        return Response({"error": "Not allowed"}, status=403)

    forms = FormRequest.objects.filter(
        is_approved=True
    ).only("id", "title")

    data = [
        {
            "id": f.id,
            "title": f.title
        }
        for f in forms
    ]

    return Response(data)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_pending_forms(request):
    if request.user.role.level <= 1:
        return Response({"error": "Not allowed"}, status=403)

    forms = FormRequest.objects.filter(
        is_approved=False
    ).only("id", "title", "current_level")

    data = [
        {
            "id": f.id,
            "title": f.title,
            "current_level": f.current_level
        }
        for f in forms
    ]

    return Response(data)
