import csv
import random
import json
from datetime import date, timedelta

current_year = date.today().year

# Base real names
base_first_names = [
    "Arun","Bala","Chandru","Dinesh","Elan","Ganesh","Hari","Irfan","Jagan","Karthik",
    "Logesh","Mani","Naveen","Omprakash","Prakash","Ramesh","Sanjay","Tharun","Umesh","Vignesh",
    "Yogesh","Ajith","Bharath","Charan","Deepak","Eswar","Gokul","Hemant","Imran","Jeeva",
    "Kishore","Lokesh","Madhan","Nithin","Praveen","Raghu","Saravanan","Tejas","Vasanth","Yuvan",
    "Anand","Boopathi","Chellam","Deva","Eashwar","Fayaz","Gopi","Harish","Ismail","Jothi",
    "Kannan","Lalit","Mohan","Naveenraj","Pandian","Ravi","Senthil","Thirumoorthy","Vel","Yasir"
]

base_last_names = [
    "Krishnan","Iyer","Rao","Selvam","Natarajan","Subramanian","Ganesan","Rajendran","Venkatesh",
    "Balaji","Sivakumar","Raghavan","Sundaram","Kuppusamy","Murugan","Perumal","Sekar","Pillai",
    "Naidu","Menon","Das","Chatterjee","Patel","Sharma","Gupta","Verma","Singh","Khan","Hussain",
    "Sheikh","Ali","Basha","Ansari","Syed","Farooq","Qureshi","Malik","Mirza","Zafar","Akhtar",
    "Chowdhury","Banerjee","Ghosh","Mukherjee","Bose","Roy","Sen","Dutta","Pal","Saha"
]

first_names = (base_first_names * 5)[:250]
last_names = (base_last_names * 5)[:250]

random.shuffle(first_names)
random.shuffle(last_names)

languages = ["Tamil", "English", "Kannada", "Hindi"]
health_support_options = ["Medication Reminders", "Mobility Assistance", "Companionship", "Doctor Appointments"]
communication_modes = ["phone", "whatsapp", "in-person"]

landmarks = [
    "Near Bus Stand",
    "Near Railway Station",
    "Near Government Hospital",
    "Opposite Temple",
    "Behind Police Station",
    "Near Market",
    "Near School",
    "Near Metro Station",
    "Near Beach Road",
    "Opposite Park"
]

def gen_phone():
    return "9" + "".join(str(random.randint(0, 9)) for _ in range(9))

def generate_dob(age):
    birth_year = current_year - age
    start_date = date(birth_year, 1, 1)
    end_date = date(birth_year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    dob = start_date + timedelta(days=random_days)
    return dob.strftime("%Y-%m-%d")

with open("elders_500(1).csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "username","email","password","full_name","phone",
        "address_line1","address_line2","city","state","pincode",
        "preferred_language","age","dob","emergency_contact_name",
        "emergency_contact_phone","health_support","communication_mode"
    ])

    for i in range(500):
        fn = first_names[i % 250]
        ln = last_names[(i * 7) % 250]

        full_name = f"{fn} {ln}"
        username = f"{fn.lower()}.{ln.lower()}{i+1}"

        age = random.randint(60, 90)
        dob = generate_dob(age)

        writer.writerow([
            username,
            f"{username}@gmail.com",
            "Welcome@123",
            full_name,
            gen_phone(),
            f"No.{i+1}, Main Street",
            random.choice(landmarks),
            "Chennai",
            "Tamil Nadu",
            f"600{random.randint(100,999)}",
            random.choice(languages),
            age,
            dob,
            f"Contact {i+1}",
            gen_phone(),
            json.dumps(random.sample(health_support_options, random.randint(1, 3))),
            random.choice(communication_modes)
        ])

print("✅ elders_500.csv generated with DOB column added correctly")