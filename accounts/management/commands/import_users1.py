import csv
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile, Volunteer

class Command(BaseCommand):
    help = "Import volunteers from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        created, skipped = 0, 0

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                username = row["username"].strip().lower()

                if User.objects.filter(username=username).exists():
                    skipped += 1
                    continue

                # 1️⃣ Create User
                user = User.objects.create_user(
                    username=username,
                    email=row["email"],
                    password=row["password"]
                )

                # 2️⃣ Create Profile
                profile = Profile.objects.create(
                    user=user,
                    role="volunteer",
                    phone=row["phone"],
                    address_line1=row["address_line1"],
                    address_line2=row["address_line2"],
                    city=row["city"],
                    state=row["state"],
                    pincode=row["pincode"],
                    preferred_language=row["preferred_language"]
                )

                # 3️⃣ Create Volunteer
                Volunteer.objects.create(
                    profile=profile,
                    skills=json.loads(row["skills"]),
                    availability=json.loads(row["availability"]),
                    experience_level=row["experience_level"],
                    is_verified=row.get("is_verified", "").lower() == "true",
                    rating=float(row.get("rating", 0.0))
                )

                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Volunteers imported successfully | Created: {created} | Skipped: {skipped}"
        ))
