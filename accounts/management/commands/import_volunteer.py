import csv
import json
from datetime import datetime
from django.contrib.auth.models import User
from accounts.models import Profile, Volunteer

with open('volunteers_500.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        # Skip if user already exists (prevents duplicate crash)
        if User.objects.filter(username=row['username']).exists():
            print(f"Skipping existing user: {row['username']}")
            continue

        # Split full name
        full_name = row['full_name'].strip().split(" ", 1)
        first_name = full_name[0]
        last_name = full_name[1] if len(full_name) > 1 else ""

        # Convert DOB string → date object
        dob_value = None
        if row.get('dob'):
            dob_value = datetime.strptime(row['dob'], "%Y-%m-%d").date()

        # Create User
        user = User.objects.create_user(
            username=row['username'],
            email=row['email'],
            password=row['password'],
            first_name=first_name,
            last_name=last_name
        )

        # Create Profile (with DOB)
        profile = Profile.objects.create(
            user=user,
            role='volunteer',
            phone=row['phone'],
            address_line1=row['address_line1'],
            address_line2=row['address_line2'],
            city=row['city'],
            state=row['state'],
            pincode=row['pincode'],
            preferred_language=row['preferred_language'],
            dob=dob_value,  # ✅ Added DOB here
        )

        # Create Volunteer
        Volunteer.objects.create(
            profile=profile,
            skills=json.loads(row['skills']) if row.get('skills') else [],
            availability=json.loads(row['availability']) if row.get('availability') else [],
            experience_level=row['experience_level'],
            is_verified=False,  # default
            rating=0.0          # default
        )

        print(f"Created volunteer: {row['username']}")

print("✅ Import completed successfully")