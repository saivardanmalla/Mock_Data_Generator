-- Sample Schema 1: Employee Table
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(15),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE,
    city VARCHAR(50),
    is_active BOOLEAN
);

-- Sample Schema 2: Student Table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(15),
    city VARCHAR(50),
    age INT,
    gender VARCHAR(10),
    admission_date DATE,
    is_active BOOLEAN
);

-- Sample Schema 3: Orders Table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    city VARCHAR(50),
    salary DECIMAL(10,2),
    order_date DATE,
    status VARCHAR(20),
    is_active BOOLEAN
);
