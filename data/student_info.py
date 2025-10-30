#!/usr/bin/env python3
"""
Student Information System - CLI
Saves data to data/students.json
"""

import json
import os
from typing import List, Dict

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def ensure_data_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_students() -> List[Dict]:
    ensure_data_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_students(students: List[Dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2, ensure_ascii=False)


def print_header():
    print()
    print("====== Student Information System ======")
    print("1. Add new student")
    print("2. View all students")
    print("3. Update a student")
    print("4. Delete a student")
    print("5. Find by ID")
    print("0. Exit")
    print()


def input_nonempty(prompt_text: str) -> str:
    while True:
        v = input(prompt_text).strip()
        if v:
            return v
        print("Input cannot be empty. Try again.")


def add_student(students: List[Dict]):
    print("\n-- Add new student --")
    sid = input_nonempty("ID: ")
    # ensure unique ID
    if any(s.get("id") == sid for s in students):
        print(f"Student with ID '{sid}' already exists.")
        return

    first = input_nonempty("First name: ")
    last = input_nonempty("Last name: ")
    while True:
        age_str = input("Age: ").strip()
        if not age_str:
            print("Age cannot be empty.")
            continue
        try:
            age = int(age_str)
            if age <= 0:
                print("Age must be positive.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for age.")
    student = {"id": sid, "first": first, "last": last, "age": age}
    students.append(student)
    save_students(students)
    print("Student added.\n")


def view_students(students: List[Dict]):
    print("\n-- All students --")
    if not students:
        print("No students found.")
        return
    # pretty table-like output
    print(f"{'ID':<12}{'First Name':<16}{'Last Name':<16}{'Age':<4}")
    print("-" * 48)
    for s in students:
        print(f"{s['id']:<12}{s['first']:<16}{s['last']:<16}{s['age']:<4}")
    print()


def find_by_id(students: List[Dict]):
    print("\n-- Find by ID --")
    sid = input_nonempty("ID: ")
    for s in students:
        if s["id"] == sid:
            print("Found:")
            print(json.dumps(s, indent=2, ensure_ascii=False))
            return
    print("Student not found.")


def update_student(students: List[Dict]):
    print("\n-- Update a student --")
    sid = input_nonempty("ID of student to update: ")
    for s in students:
        if s["id"] == sid:
            print("Leave blank to keep current value.")
            new_first = input(f"First name [{s['first']}]: ").strip() or s['first']
            new_last = input(f"Last name [{s['last']}]: ").strip() or s['last']
            while True:
                new_age_str = input(f"Age [{s['age']}]: ").strip()
                if not new_age_str:
                    new_age = s['age']
                    break
                try:
                    new_age = int(new_age_str)
                    if new_age <= 0:
                        print("Age must be positive.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid integer.")
            s.update({"first": new_first, "last": new_last, "age": new_age})
            save_students(students)
            print("Student updated.")
            return
    print("Student not found.")


def delete_student(students: List[Dict]):
    print("\n-- Delete a student --")
    sid = input_nonempty("ID to delete: ")
    for i, s in enumerate(students):
        if s["id"] == sid:
            confirm = input(f"Confirm delete {s['first']} {s['last']} (y/N): ").strip().lower()
            if confirm == "y":
                students.pop(i)
                save_students(students)
                print("Student deleted.")
            else:
                print("Delete cancelled.")
            return
    print("Student not found.")


def main():
    students = load_students()
    while True:
        print_header()
        choice = input("Select a number: ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            update_student(students)
        elif choice == "4":
            delete_student(students)
        elif choice == "5":
            find_by_id(students)
        elif choice == "0":
            print("Thankyou,Come Again!")
            break
        else:
            print("Invalid option. Choose 0-5.\n")


if __name__ == "__main__":
    main()

