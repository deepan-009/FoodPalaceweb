"""
Bulk-load Google Maps reviews from a JSON or CSV file.

    python manage.py import_reviews core/data/reviews.json
    python manage.py import_reviews core/data/reviews.csv --replace

JSON: a list of objects. CSV: a header row using the same field names.
Only `user_name`, `rating` and `text` are required; everything else is optional.
"""

import csv
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from core.models import Review

FIELDS = {f.name for f in Review._meta.get_fields() if hasattr(f, "attname")}
INT_FIELDS = {
    "rating", "review_count", "photo_count", "likes", "order",
    "food_rating", "service_rating", "atmosphere_rating",
}
BOOL_FIELDS = {"is_local_guide", "is_edited", "is_featured"}
TRUTHY = {"1", "true", "yes", "y", "on"}


class Command(BaseCommand):
    help = "Import reviews from a JSON or CSV file."

    def add_arguments(self, parser):
        parser.add_argument("path", help="Path to a .json or .csv file")
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete all existing reviews before importing.",
        )

    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"No file at {path}")

        if path.suffix.lower() == ".json":
            rows = json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix.lower() == ".csv":
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
        else:
            raise CommandError("Use a .json or .csv file.")

        if options["replace"]:
            deleted, _ = Review.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Removed {deleted} existing reviews."))

        created = skipped = 0
        for position, row in enumerate(rows, start=1):
            data = {}
            for key, value in row.items():
                key = key.strip()
                if key not in FIELDS or key in {"id", "created_at"}:
                    continue
                if value in ("", None):
                    continue
                if key in INT_FIELDS:
                    try:
                        value = int(float(value))
                    except (TypeError, ValueError):
                        continue
                elif key in BOOL_FIELDS:
                    value = str(value).strip().lower() in TRUTHY if not isinstance(value, bool) else value
                data[key] = value

            if not data.get("user_name") or not data.get("text"):
                skipped += 1
                continue
            data.setdefault("rating", 5)
            data.setdefault("order", position)

            Review.objects.update_or_create(
                user_name=data["user_name"],
                time_ago=data.get("time_ago", ""),
                defaults=data,
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Imported {created} reviews. Skipped {skipped} incomplete rows.")
        )
        self.stdout.write(f"Total in database: {Review.objects.count()}")
