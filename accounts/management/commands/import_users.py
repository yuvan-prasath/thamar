import csv
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile, Elder, Volunteer

class Command(BaseCommand):
    help = "Import users from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)
        parser.add_argument("role", type=str)  # elder / volunteer

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        role = options["role"].lower()

        if role not in ["elder", "volunteer"]:
            self.stdout.write(self.style.ERROR("Role must be 'elder' or 'volunteer'"))
            return

        created = 0
        skipped = 0

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                username = row["username"]

                if User.objects.filter(username=username).exists():
                    skipped += 1
                    continue

                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=row["email"],
                    password=row["password"],
                    first_name=row["full_name"].split(" ")[0],
                    last_name=" ".join(row["full_name"].split(" ")[1:])
                )

                # Create profile
                profile = Profile.objects.create(
                    user=user,
                    role=role,
                    phone=row["phone"],
                    address_line1=row["address_line1"],
                    address_line2=row["address_line2"],
                    city=row["city"],
                    state=row["state"],
                    pincode=row["pincode"],
                    preferred_language=row["preferred_language"],
                )

                if role == "elder":
                    Elder.objects.create(
                        profile=profile,
                        age=int(row["age"]),
                        emergency_contact_name=row["emergency_contact_name"],
                        emergency_contact_phone=row["emergency_contact_phone"],
                        health_support=json.loads(row["health_support"]),
                        communication_mode=row["communication_mode"]
                    )

                elif role == "volunteer":
                    Volunteer.objects.create(
                        profile=profile,
                        skills=json.loads(row.get("skills", "[]")),
                        availability=json.loads(row.get("availability", "[]")),
                        experience_level=row.get("experience_level", "Beginner"),
                        is_verified=False,
                        rating=0.0
                    )

                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Imported: {created} users"))
        self.stdout.write(self.style.WARNING(f"⚠️ Skipped duplicates: {skipped} users"))
