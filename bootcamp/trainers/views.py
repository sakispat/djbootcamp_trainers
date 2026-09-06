"""Views for trainer management."""

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .forms import TrainerForm
from .models import Trainer


@require_http_methods(["GET"])
def index(request):
    """Display trainers with stable ordering and pagination."""
    trainers = Trainer.objects.order_by(
        "last_name",
        "first_name",
        "pk",
    )

    paginator = Paginator(trainers, 6)
    trainer_lists = paginator.get_page(request.GET.get("page"))

    context = {
        "trainer_lists": trainer_lists,
    }

    return render(
        request,
        "trainers/index.html",
        context,
    )


@require_http_methods(["GET", "POST"])
def create_trainer(request):
    """Create a trainer and preserve invalid form input."""
    if request.method == "POST":
        form = TrainerForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Trainer created successfully.",
            )

            return redirect("home")

    else:
        form = TrainerForm()

    return render(
        request,
        "trainers/create.html",
        {"form": form},
    )


@require_http_methods(["GET", "POST"])
def update_trainer(request, trainer_id):
    """Update the selected trainer without creating a new record."""
    trainer = get_object_or_404(
        Trainer,
        pk=trainer_id,
    )

    if request.method == "POST":
        form = TrainerForm(
            request.POST,
            instance=trainer,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Trainer updated successfully.",
            )

            return redirect("home")

    else:
        form = TrainerForm(instance=trainer)

    context = {
        "form": form,
        "trainer": trainer,
    }

    return render(
        request,
        "trainers/edit.html",
        context,
    )


@require_http_methods(["GET", "POST"])
def delete_trainer(request, trainer_id):
    """Show confirmation on GET and delete only on POST."""
    trainer = get_object_or_404(
        Trainer,
        pk=trainer_id,
    )

    if request.method == "POST":
        trainer.delete()

        messages.success(
            request,
            "Trainer deleted successfully.",
        )

        return redirect("home")

    return render(
        request,
        "trainers/delete_confirm.html",
        {"trainer": trainer},
    )


@require_http_methods(["GET", "POST"])
def search_trainer(request):
    """Search by surname while supporting the existing POST form."""
    # Keep POST support until the search template is migrated to GET.
    parameters = (
        request.POST
        if request.method == "POST"
        else request.GET
    )

    query = parameters.get("q", "").strip()
    results = Trainer.objects.none()

    if query:
        results = Trainer.objects.filter(
            last_name__icontains=query,
        ).order_by(
            "last_name",
            "first_name",
            "pk",
        )

    context = {
        "results": results,
        "query": query,
    }

    return render(
        request,
        "trainers/search.html",
        context,
    )