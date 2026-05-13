# CSV Data Processor

A Python-based CSV data processing and machine learning project built using Object-Oriented Programming principles. The system reads, validates, processes, and classifies Iris dataset samples using the k-Nearest Neighbours (k-NN) algorithm and multiple distance calculation techniques.

---

## Features

- CSV file reading and writing
- Automatic training/testing dataset splitting
- Data validation and corruption handling
- k-NN classification algorithm
- Multiple distance algorithms:
  - Euclidean Distance
  - Manhattan Distance
  - Chebyshev Distance
  - Sorensen Distance
- Object-Oriented design
- Dynamic sample classification
- Statistical testing and accuracy evaluation
- Monkey patching methods at runtime
- Error handling using custom exceptions

---

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- CSV Processing
- k-Nearest Neighbours (k-NN)
- Dynamic Method Binding
- Type Hinting
- File Handling

---

## Project Structure

```bash
.
├── model.py
├── data_processor.py
├── data_keys.py
├── iris.csv
└── README.md
```

---

## How It Works

1. The program reads CSV data from the Iris dataset.
2. Data is validated and corrupted rows are detected.
3. Samples are split into:
   - Training Data
   - Testing Data
4. Multiple distance algorithms are used to calculate similarity between samples.
5. The k-NN algorithm classifies unknown samples.
6. Accuracy and classification quality are evaluated.

---

## Key Concepts Demonstrated

- Object-Oriented Programming
- Inheritance and Polymorphism
- Abstract Classes
- Protocols and Type Hinting
- File Processing
- Machine Learning Fundamentals
- Data Validation
- Dynamic Method Injection (Monkey Patching)

---

## Running the Program

```bash
python data_processor.py
```

---

## Example Output

```text
--- Read data from iris.csv (total=150, training=120, testing=30)

### WARNING: Row 24: Invalid species in {...}

Classification Quality: 0.93
```

---

## Distance Algorithms Implemented

- Euclidean Distance
- Manhattan Distance
- Chebyshev Distance
- Sorensen Distance
- Generalized Minkowski Distance

---

## Learning Outcomes

This project strengthened understanding of:

- Python OOP architecture
- CSV data manipulation
- Machine learning classification basics
- Error handling and validation
- Algorithm implementation
- Data modelling and abstraction

---

## Author

Joy Saina  
Software Engineering Student  
Middle East Technical University (METU NCC)
