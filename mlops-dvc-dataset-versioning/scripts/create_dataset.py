import csv
from pathlib import Path


students = [
    {
        "student_id": 1001,
        "name": "Aarav Sharma",
        "roll_no": "CSE001",
        "department": "CSE",
        "year": 3,
        "attendance": 92,
        "marks": 88,
        "grade": "A"
    },
    {
        "student_id": 1002,
        "name": "Aditya Patil",
        "roll_no": "CSE002",
        "department": "CSE",
        "year": 3,
        "attendance": 85,
        "marks": 76,
        "grade": "B"
    },
    {
        "student_id": 1003,
        "name": "Sneha Kulkarni",
        "roll_no": "AI003",
        "department": "AI",
        "year": 3,
        "attendance": 95,
        "marks": 91,
        "grade": "A+"
    },
    {
        "student_id": 1004,
        "name": "Riya Deshmukh",
        "roll_no": "AI004",
        "department": "AI",
        "year": 3,
        "attendance": 89,
        "marks": 84,
        "grade": "A"
    },
    {
        "student_id": 1005,
        "name": "Rahul Joshi",
        "roll_no": "DS005",
        "department": "DS",
        "year": 3,
        "attendance": 78,
        "marks": 69,
        "grade": "B"
    },
    {
        "student_id": 1006,
        "name": "Priya Mehta",
        "roll_no": "DS006",
        "department": "DS",
        "year": 3,
        "attendance": 94,
        "marks": 87,
        "grade": "A"
    },
    {
        "student_id": 1007,
        "name": "Kunal Shah",
        "roll_no": "CSE007",
        "department": "CSE",
        "year": 3,
        "attendance": 81,
        "marks": 73,
        "grade": "B"
    },
    {
        "student_id": 1008,
        "name": "Isha More",
        "roll_no": "AI008",
        "department": "AI",
        "year": 3,
        "attendance": 97,
        "marks": 94,
        "grade": "A+"
    },
    {
        "student_id": 1009,
        "name": "Vivek Pawar",
        "roll_no": "CSE009",
        "department": "CSE",
        "year": 3,
        "attendance": 74,
        "marks": 65,
        "grade": "C"
    },
    {
        "student_id": 1010,
        "name": "Ananya Joshi",
        "roll_no": "DS010",
        "department": "DS",
        "year": 3,
        "attendance": 91,
        "marks": 89,
        "grade": "A"
    },
    {
        "student_id": 1011,
        "name": "Rohan Patil",
        "roll_no": "CSE011",
        "department": "CSE",
        "year": 3,
        "attendance": 88,
        "marks": 80,
        "grade": "A"
    },
    {
        "student_id": 1012,
        "name": "Neha Jadhav",
        "roll_no": "AI012",
        "department": "AI",
        "year": 3,
        "attendance": 83,
        "marks": 72,
        "grade": "B"
    },
    {
        "student_id": 1013,
        "name": "Siddhant Kale",
        "roll_no": "DS013",
        "department": "DS",
        "year": 3,
        "attendance": 90,
        "marks": 86,
        "grade": "A"
    },
    {
        "student_id": 1014,
        "name": "Tanvi Pawar",
        "roll_no": "AI014",
        "department": "AI",
        "year": 3,
        "attendance": 96,
        "marks": 93,
        "grade": "A+"
    },
    {
        "student_id": 1015,
        "name": "Akash Chavan",
        "roll_no": "CSE015",
        "department": "CSE",
        "year": 3,
        "attendance": 79,
        "marks": 68,
        "grade": "B"
    },
]


output_file = Path("data/raw/students.csv")

output_file.parent.mkdir(parents=True, exist_ok=True)

fieldnames = students[0].keys()

with output_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(students)

print(f"Dataset created successfully: {output_file}")
print(f"Number of students: {len(students)}")