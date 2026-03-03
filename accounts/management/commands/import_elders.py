import csv
import json
from datetime import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile, Elder


class Command(BaseCommand):
    help = "Import elders from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to CSV file")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        created_count = 0
        skipped_count = 0

        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                username = row.get("username")

                # Skip if username exists
                if User.objects.filter(username=username).exists():
                    self.stdout.write(
                        self.style.WARNING(f"Skipped (exists): {username}")
                    )
                    skipped_count += 1
                    continue

                # Parse DOB
                dob = None
                if row.get("dob"):
                    try:
                        dob = datetime.strptime(row["dob"], "%Y-%m-%d").date()
                    except ValueError:
                        self.stdout.write(
                            self.style.WARNING(f"Invalid DOB for {username}")
                        )

                # Split full name
                full_name = row.get("full_name", "").strip()
                name_parts = full_name.split(" ", 1)
                first_name = name_parts[0] if name_parts else ""
                last_name = name_parts[1] if len(name_parts) > 1 else ""

                # 1️⃣ Create User
                user = User.objects.create_user(
                    username=username,
                    password=row.get("password"),
                    email=row.get("email", ""),
                    first_name=first_name,
                    last_name=last_name,
                )

                # 2️⃣ Create Profile (COMMON DATA + DOB)
                profile = Profile.objects.create(
                    user=user,
                    role="elder",
                    phone=row.get("phone", ""),
                    address_line1=row.get("address_line1", ""),
                    address_line2=row.get("address_line2", ""),
                    city=row.get("city", ""),
                    state=row.get("state", ""),
                    pincode=row.get("pincode", ""),
                    preferred_language=row.get("preferred_language", ""),
                    dob=dob,
                )

                # Parse health_support JSON safely
                health_data = None
                if row.get("health_support"):
                    try:
                        health_data = json.loads(row["health_support"])
                    except:
                        health_data = row["health_support"].split(",")

                # 3️⃣ Create Elder (ELDER-SPECIFIC DATA)
                Elder.objects.create(
                    profile=profile,
                    emergency_contact_name=row.get("emergency_contact_name", ""),
                    emergency_contact_phone=row.get("emergency_contact_phone", ""),
                    health_support=health_data,
                    communication_mode=row.get("communication_mode", ""),
                )

                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {username}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nImport Complete → Created: {created_count}, Skipped: {skipped_count}"
            )
        )