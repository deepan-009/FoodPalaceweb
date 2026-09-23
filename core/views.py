from django.contrib import messages
from django.db.models import Avg, Count, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BookingForm
from .models import Award, Kitchen, MenuCategory, MenuItem, Review


def _categories(kitchen=None):
    qs = MenuCategory.objects.prefetch_related(
        Prefetch("items", queryset=MenuItem.objects.order_by("order", "name"))
    )
    if kitchen:
        qs = qs.filter(kitchen=kitchen)
    return qs


def home(request):
    signatures = MenuItem.objects.filter(is_signature=True).select_related("category")[:8]
    featured = Review.objects.filter(is_featured=True)[:6]
    stats = Review.objects.aggregate(avg=Avg("rating"), total=Count("id"))
    context = {
        "signatures": signatures,
        "featured_reviews": featured,
        "awards": Award.objects.filter(is_highlight=True)[:4],
        "kitchens": Kitchen.choices,
        "review_avg": round(stats["avg"], 1) if stats["avg"] else None,
        "review_total": stats["total"],
        "active": "home",
    }
    return render(request, "pages/home.html", context)


def menu(request):
    kitchen = request.GET.get("kitchen") or ""
    valid = dict(Kitchen.choices)
    if kitchen not in valid:
        kitchen = ""

    categories = _categories(kitchen or None)
    grouped = []
    for key, label in Kitchen.choices:
        cats = [c for c in categories if c.kitchen == key]
        if cats:
            grouped.append({"key": key, "label": label, "categories": cats})

    context = {
        "grouped": grouped,
        "kitchens": Kitchen.choices,
        "active_kitchen": kitchen,
        "item_total": MenuItem.objects.count(),
        "active": "menu",
    }
    return render(request, "pages/menu.html", context)


def about(request):
    return render(request, "pages/about.html", {"active": "about"})


def awards(request):
    context = {
        "awards": Award.objects.all(),
        "highlights": Award.objects.filter(is_highlight=True),
        "active": "awards",
    }
    return render(request, "pages/awards.html", context)


def reviews(request):
    qs = Review.objects.all()

    rating = request.GET.get("rating")
    if rating in {"1", "2", "3", "4", "5"}:
        qs = qs.filter(rating=int(rating))

    sort = request.GET.get("sort", "")
    if sort == "highest":
        qs = qs.order_by("-rating", "order")
    elif sort == "lowest":
        qs = qs.order_by("rating", "order")
    elif sort == "liked":
        qs = qs.order_by("-likes", "order")

    breakdown = []
    total = Review.objects.count()
    counts = {
        row["rating"]: row["n"]
        for row in Review.objects.values("rating").annotate(n=Count("id"))
    }
    for star in range(5, 0, -1):
        n = counts.get(star, 0)
        breakdown.append(
            {"star": star, "count": n, "pct": round((n / total) * 100) if total else 0}
        )

    stats = Review.objects.aggregate(avg=Avg("rating"))
    context = {
        "reviews": qs,
        "breakdown": breakdown,
        "review_total": total,
        "review_avg": round(stats["avg"], 1) if stats["avg"] else None,
        "active_rating": rating or "",
        "active_sort": sort,
        "active": "reviews",
    }
    return render(request, "pages/reviews.html", context)


def contact(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(
                request,
                f"Thanks {booking.name}, we have your request. "
                "The counter will call you back on that number.",
            )
            return redirect("core:contact")
        messages.error(request, "Check the highlighted fields and send it again.")
    else:
        form = BookingForm()
    return render(request, "pages/contact.html", {"form": form, "active": "contact"})


@require_POST
def like_review(request, pk):
    """Small AJAX endpoint behind the Like button on each review card."""
    review = get_object_or_404(Review, pk=pk)
    liked_ids = set(request.session.get("liked_reviews", []))
    if pk in liked_ids:
        review.likes = max(0, review.likes - 1)
        liked_ids.discard(pk)
        liked = False
    else:
        review.likes += 1
        liked_ids.add(pk)
        liked = True
    review.save(update_fields=["likes"])
    request.session["liked_reviews"] = list(liked_ids)
    return JsonResponse({"likes": review.likes, "liked": liked})
