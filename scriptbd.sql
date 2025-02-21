DROP DATABASE IF EXISTS todolist;

CREATE DATABASE todolist;

USE todolist;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao TEXT NOT NULL,
    data DATE NOT NULL,
    status ENUM('Pendente', 'Concluída') DEFAULT 'Pendente'
);

