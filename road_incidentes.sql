CREATE TABLE road_incidents (
    id INT PRIMARY KEY AUTO_INCREMENT,   -- ID único do registro
    created_at TIMESTAMP NOT NULL, -- data e hora
    road_name VARCHAR(255) NOT NULL, -- Nome da estrada, limite de 255 caracteres
    vehicle VARCHAR(100) NOT NULL, -- Tipo de veículo, limite de 100 caracteres
    number_deaths INT NOT NULL -- Número de incidentes
);