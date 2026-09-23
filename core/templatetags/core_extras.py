from django import template

register = template.Library()


@register.filter
def stars(value):
    """{% for _ in review.rating|stars %} -> one pass per filled star."""
    try:
        return range(int(value))
    except (TypeError, ValueError):
        return range(0)


@register.filter
def empty_stars(value):
    try:
        return range(5 - int(value))
    except (TypeError, ValueError):
        return range(5)


@register.filter
def split_price(value):
    """'160/300' -> ['160', '300'] so half/full prices can be styled apart."""
    return [p.strip() for p in str(value).split("/") if p.strip()]


@register.filter
def liked_by(review, request):
    return review.pk in set(request.session.get("liked_reviews", []))
