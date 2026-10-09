CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendedor VARCHAR(100) NOT NULL,
    sede VARCHAR(100) NOT NULL,
    producto VARCHAR(150) NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(12, 2) NOT NULL,
    fecha DATE NOT NULL
);

INSERT INTO ventas (vendedor, sede, producto, cantidad, precio, fecha)
VALUES
    ('Ana Torres', 'Bogotá', 'Laptop', 3, 3500000.00, '2026-09-01'),
    ('Carlos Ruiz', 'Medellín', 'Mouse', 15, 45000.00, '2026-09-02'),
    ('Laura Gómez', 'Bogotá', 'Teclado', 8, 120000.00, '2026-09-03'),
    ('Ana Torres', 'Cali', 'Monitor', 4, 850000.00, '2026-09-04'),
    ('Carlos Ruiz', 'Medellín', 'Laptop', 2, 3500000.00, '2026-09-05'),
    ('Laura Gómez', 'Bogotá', 'Mouse', 20, 45000.00, '2026-09-06'),
    ('Pedro Díaz', 'Cali', 'Teclado', 10, 120000.00, '2026-09-07'),
    ('Ana Torres', 'Medellín', 'Monitor', 5, 850000.00, '2026-09-08'),
    ('Pedro Díaz', 'Bogotá', 'Laptop', 1, 3500000.00, '2026-09-09'),
    ('Carlos Ruiz', 'Cali', 'Mouse', 12, 45000.00, '2026-09-10');