from django.db import models
from django.utils.text import slugify


class Kitchen(models.TextChoices):
    """Food Palace runs three counters under one roof."""

    FOOD_PALACE = "food_palace", "Food Palace"
    BROASTED_KING = "broasted_king", "Broasted King"
    JUICE_PALACE = "juice_palace", "Juice Palace"


class MenuCategory(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    kitchen = models.CharField(
        max_length=20, choices=Kitchen.choices, default=Kitchen.FOOD_PALACE
    )
    blurb = models.CharField(
        max_length=180,
        blank=True,
        help_text="One line shown under the category heading.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "menu categories"
        ordering = ["kitchen", "order", "name"]

    def __str__(self):
        return f"{self.get_kitchen_display()} — {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.kitchen}-{self.name}")[:85]
            slug, n = base, 2
            while MenuCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class MenuItem(models.Model):
    category = models.ForeignKey(
        MenuCategory, related_name="items", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=200, blank=True)
    # Free text so the real menu card can be reproduced exactly:
    # "200", "160/300" (half/full), "Season", "440/230/120" (full/half/quarter).
    price = models.CharField(max_length=40, blank=True)
    is_veg = models.BooleanField(default=False)
    is_signature = models.BooleanField(
        default=False, help_text="Shows a flame mark and appears in Home highlights."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name

    @property
    def price_display(self):
        value = (self.price or "").strip()
        if not value:
            return "—"
        if not value[0].isdigit():
            return value  # "Season", "Ask counter", etc.
        return "₹" + value

    @property
    def price_parts(self):
        """['160', '300'] for split half/full pricing, else a single value."""
        return [p.strip() for p in (self.price or "").split("/") if p.strip()]


class Review(models.Model):
    """One Google Maps review. Add as many as you like from /admin/."""

    user_name = models.CharField(max_length=120)
    profile_pic_url = models.URLField(
        blank=True, help_text="Leave blank to use a generated initial avatar."
    )
    is_local_guide = models.BooleanField(default=False)
    review_count = models.PositiveIntegerField(default=0)
    photo_count = models.PositiveIntegerField(default=0)

    rating = models.PositiveSmallIntegerField(
        default=5, choices=[(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)]
    )
    time_ago = models.CharField(max_length=40, default="a year ago")
    is_edited = models.BooleanField(default=False)
    text = models.TextField()

    # Optional detail block Google shows under some reviews.
    order_type = models.CharField(max_length=40, blank=True)
    meal_type = models.CharField(max_length=40, blank=True)
    price_range = models.CharField(max_length=40, blank=True)
    food_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    service_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    atmosphere_rating = models.PositiveSmallIntegerField(null=True, blank=True)

    likes = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(
        default=False, help_text="Featured reviews appear on the home page."
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.user_name} ({self.rating}★)"

    @property
    def initial(self):
        return (self.user_name or "?").strip()[:1].upper()

    @property
    def stars_filled(self):
        return range(self.rating)

    @property
    def stars_empty(self):
        return range(5 - self.rating)

    @property
    def avatar_seed(self):
        """Stable 0-5 index so each person keeps the same avatar colour."""
        return sum(ord(c) for c in self.user_name) % 6

    @property
    def has_detail_block(self):
        return any(
            [
                self.order_type,
                self.meal_type,
                self.price_range,
                self.food_rating,
                self.service_rating,
                self.atmosphere_rating,
            ]
        )


class Award(models.Model):
    title = models.CharField(max_length=140)
    issuer = models.CharField(max_length=120, blank=True)
    year = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    metric = models.CharField(
        max_length=40, blank=True, help_text="Big number, e.g. '1,059' or '3.8'."
    )
    metric_label = models.CharField(max_length=60, blank=True)
    is_highlight = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-year"]

    def __str__(self):
        return self.title


class Booking(models.Model):
    """Table request or catering enquiry sent from the contact page."""

    OCCASION_CHOICES = [
        ("table", "Table for tonight"),
        ("party", "Party or group booking"),
        ("catering", "Catering enquiry"),
        ("feedback", "Feedback for the kitchen"),
    ]

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    occasion = models.CharField(
        max_length=20, choices=OCCASION_CHOICES, default="table"
    )
    guests = models.PositiveIntegerField(default=2)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} · {self.get_occasion_display()}"
