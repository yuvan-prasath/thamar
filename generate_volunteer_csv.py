import csv
import random
import json
from datetime import date, timedelta

first_names = [
    "Arun","Bala","Chandru","Dinesh","Elan","Ganesh","Hari","Irfan","Jagan","Karthik",
    "Logesh","Mani","Naveen","Omprakash","Prakash","Ramesh","Sanjay","Tharun","Umesh","Vignesh",
    "Yogesh","Ajith","Bharath","Charan","Deepak","Eswar","Gokul","Hemant","Imran","Jeeva",
    "Kishore","Lokesh","Madhan","Nithin","Praveen","Raghu","Saravanan","Tejas","Vasanth","Yuvan",
    "Anand","Boopathi","Deva","Eashwar","Fayaz","Gopi","Harish","Ismail","Jothi","Kannan"
]

last_names = [
    "Krishnan","Iyer","Rao","Selvam","Natarajan","Subramanian","Ganesan","Rajendran","Venkatesh",
    "Balaji","Sivakumar","Raghavan","Sundaram","Kuppusamy","Murugan","Perumal","Sekar","Pillai",
    "Naidu","Menon","Das","Patel","Sharma","Gupta","Verma","Singh","Khan","Hussain","Sheikh","Ali",
    "Basha","Ansari","Syed","Farooq","Qureshi","Malik","Mirza","Zafar","Akhtar","Roy","Sen","Pal",
    "Saha","Ghosh","Bose","Banerjee","Mukherjee","Dutta","Chowdhury","Chatterjee"
]

skills_options = ["Medical", "Companionship", "Errands", "Tech Help"]
availability_options = ["Morning", "Evening", "Weekends"]
languages = ["Tamil", "English", "Hindi", "Kannada"]
landmarks = ["Near Bus Stand", "Near Railway Station", "Near Metro Station", "Opposite Park", "Near Hospital"]

def gen_phone():
    return "9" + "".join(str(random.randint(0, 9)) for _ in range(9))

def gen_dob():
    # Generate DOB between 18 and 60 years old
    today = date.today()
    min_age = 18
    max_age = 60
    
    start_date = today - timedelta(days=365 * max_age)
    end_date = today - timedelta(days=365 * min_age)
    
    random_days = random.randint(0, (end_date - start_date).days)
    dob = start_date + timedelta(days=random_days)
    return dob.strftime("%Y-%m-%d")

with open("volunteers_500.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "username","email","password","full_name","phone",
        "address_line1","address_line2","city","state","pincode",
        "preferred_language","dob","skills","availability","experience_level"
    ])

    for i in range(500):
        fn = first_names[i % len(first_names)]
        ln = last_names[(i * 3) % len(last_names)]

        username = f"{fn.lower()}{ln.lower()}{i+1}"

        writer.writerow([
            username,
            f"{username}@gmail.com",
            "Welcome@123",
            f"{fn} {ln}",
            gen_phone(),
            f"No.{i+1}, Main Street",
            random.choice(landmarks),
            "Chennai",
            "Tamil Nadu",
            f"600{random.randint(100,999)}",
            random.choice(languages),
            gen_dob(),  # ✅ Added DOB
            json.dumps(random.sample(skills_options, random.randint(1, 3))),
            json.dumps(random.sample(availability_options, random.randint(1, 2))),
            random.choice(["Beginner","Intermediate","Experienced"])
        ])

print("✅ volunteers_500.csv generated successfully")