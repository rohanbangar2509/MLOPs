# Dataset Versioning Using DVC

## Overview

This project demonstrates **dataset versioning using Data Version Control (DVC)** as part of an MLOps workflow.

A small synthetic student dataset is used to demonstrate how datasets can be versioned independently from source code while Git is used to track the corresponding DVC metadata.

The project demonstrates:

* Dataset creation
* DVC initialization
* Dataset tracking with DVC
* Local DVC remote storage
* Dataset versioning
* Dataset modification
* Dataset reproduction
* Switching between dataset versions
* Git and DVC integration

---

## Problem Statement

In machine learning projects, datasets change over time.

For example:

* New records may be added.
* Existing records may be corrected.
* Features may be modified.
* Incorrect data may be removed.

If the dataset is stored directly inside Git, repositories can become unnecessarily large and difficult to manage.

DVC solves this problem by allowing large datasets to be versioned separately while Git tracks lightweight metadata describing which dataset version should be used.

---

## Objectives

The main objectives of this project are:

1. Understand the need for dataset versioning.
2. Learn how to initialize DVC.
3. Track datasets using DVC.
4. Configure a DVC remote.
5. Store dataset versions outside Git.
6. Track dataset changes using Git commits.
7. Reproduce previous dataset versions.
8. Understand how Git and DVC work together.

---

## Technology Stack

| Technology | Purpose                             |
| ---------- | ----------------------------------- |
| Python     | Dataset generation                  |
| Git        | Source-code and metadata versioning |
| DVC        | Dataset versioning                  |
| CSV        | Dataset format                      |
| PowerShell | Windows command-line environment    |

---

## Dataset

A synthetic student dataset containing 15 student records was created using Python dictionaries.

### Dataset Features

| Column       | Description               |
| ------------ | ------------------------- |
| `student_id` | Unique student identifier |
| `name`       | Student name              |
| `roll_no`    | Student roll number       |
| `department` | Academic department       |
| `year`       | Current academic year     |
| `attendance` | Attendance percentage     |
| `marks`      | Examination marks         |
| `grade`      | Student grade             |

Example:

```text
student_id,name,roll_no,department,year,attendance,marks,grade
1001,Aarav Sharma,CSE001,CSE,3,92,88,A
1002,Aditya Patil,CSE002,CSE,3,85,76,B
1003,Sneha Kulkarni,AI003,AI,3,95,91,A+
```

---

## Project Structure

```text
mlops-dvc-dataset-versioning/
│
├── data/
│   └── raw/
│       ├── students.csv
│       └── students.csv.dvc
│
├── scripts/
│   └── create_dataset.py
│
├── .dvc/
│   ├── .gitignore
│   └── config
│
├── .gitignore
└── README.md
```

---

# Installation

## Prerequisites

Install the following software on Windows:

* Python
* Git
* DVC

Verify Python:

```powershell
python --version
```

Verify Git:

```powershell
git --version
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Install DVC:

```powershell
pip install dvc
```

Verify DVC:

```powershell
dvc --version
```

---

# Initialize the Project

Initialize Git:

```powershell
git init
```

Initialize DVC:

```powershell
dvc init
```

---

# Create the Dataset

Run:

```powershell
python scripts\create_dataset.py
```

The script creates:

```text
data/raw/students.csv
```

---

# Track the Dataset Using DVC

Add the dataset to DVC:

```powershell
dvc add data/raw/students.csv
```

This creates:

```text
data/raw/students.csv.dvc
```

The `.dvc` file contains metadata required by DVC to identify the dataset version.

---

# Configure DVC Remote

For this learning project, a local directory is used as the DVC remote.

Create the directory:

```powershell
mkdir dvc-storage
```

Configure the remote:

```powershell
dvc remote add -d local-storage dvc-storage
```

Verify:

```powershell
dvc remote list
```

---

# Push Dataset to DVC Storage

Run:

```powershell
dvc push
```

The dataset is now stored in the configured DVC remote.

Git does not need to store the actual dataset contents.

---

# Commit Dataset Version 1

Check the repository:

```powershell
git status
```

Add the files:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Add student dataset version 1 with DVC"
```

At this point, Git tracks the DVC metadata while DVC manages the actual dataset.

---

# Create Dataset Version 2

Modify:

```text
data/raw/students.csv
```

For example:

* Add a new student.
* Change an existing student's marks.
* Update a grade.

Run:

```powershell
dvc status
```

DVC will detect that the dataset has changed.

Update the DVC metadata:

```powershell
dvc add data/raw/students.csv
```

Push the new dataset version:

```powershell
dvc push
```

Commit the new version:

```powershell
git add data/raw/students.csv.dvc
git commit -m "Update student dataset to version 2"
```

---

# Dataset Versioning Workflow

The overall workflow is:

```text
              ┌─────────────────┐
              │ Student Dataset │
              └────────┬────────┘
                       │
                       ▼
                 ┌───────────┐
                 │    DVC    │
                 └─────┬─────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
      Dataset Storage      .dvc Metadata
             │                   │
             │                   ▼
             │                 Git
             │                   │
             ▼                   ▼
       Dataset Version     Code + Metadata
```

---

# Reproduce a Previous Version

View Git history:

```powershell
git log --oneline
```

Example:

```text
8f32abc Update student dataset to version 2
21ab456 Add student dataset version 1 with DVC
```

Checkout the previous DVC metadata:

```powershell
git checkout 21ab456 -- data/raw/students.csv.dvc
```

Then restore the corresponding dataset:

```powershell
dvc checkout
```

The dataset will now correspond to the selected Git version.

---

# Useful DVC Commands

### Check DVC status

```powershell
dvc status
```

### Add a dataset

```powershell
dvc add data/raw/students.csv
```

### Push dataset

```powershell
dvc push
```

### Pull dataset

```powershell
dvc pull
```

### Restore tracked data

```powershell
dvc checkout
```

### Show configured remotes

```powershell
dvc remote list
```

### Show DVC files

```powershell
dvc list .
```

---

# Git and DVC Responsibilities

Git and DVC serve different purposes.

### Git

Git tracks:

```text
Source code
README
Configuration
DVC metadata
Project history
```

### DVC

DVC tracks:

```text
Datasets
Large files
Dataset versions
Data storage
Data reproduction
```

Together:

```text
Git
 +
DVC
 =
Reproducible ML Data Workflow
```

---

# Why DVC Is Useful in MLOps

Dataset versioning is important because an ML model is dependent on the data used to train it.

Consider:

```text
Dataset Version 1
       ↓
   Model V1
```

Later:

```text
Dataset Version 2
       ↓
   Model V2
```

Without dataset versioning, it becomes difficult to determine exactly which data produced a particular model.

With DVC:

```text
Git Commit A
     │
     └── Dataset V1
             │
             └── Model V1


Git Commit B
     │
     └── Dataset V2
             │
             └── Model V2
```

This improves reproducibility and experiment management.

---

# Learning Outcomes

After completing this project, the following concepts are understood:

* Why datasets should be versioned
* Difference between Git and DVC
* DVC initialization
* DVC dataset tracking
* DVC remotes
* Dataset version creation
* Dataset modification tracking
* Dataset reproduction
* Git-DVC integration
* Basic MLOps data management

---

# Future Improvements

This project can later be extended with:

* Remote DVC storage using AWS S3
* Model versioning
* MLflow experiment tracking
* DVC pipelines
* Automated CI/CD
* Data validation
* Model deployment
* Data and model monitoring

---

## Conclusion

This project demonstrates a basic but complete MLOps workflow for dataset versioning using DVC.

Git manages the project history and DVC metadata, while DVC manages the actual dataset versions.

This separation makes machine learning projects more reproducible, manageable, and scalable.
