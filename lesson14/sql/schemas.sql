CREATE DATABASE IF NOT EXISTS bus_fleet
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE bus_fleet;

CREATE TABLE IF NOT EXISTS companies (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(120) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_companies_name (name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS buses (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    plate_number VARCHAR(15) NOT NULL,
    model VARCHAR(80) NOT NULL,
    seats INT UNSIGNED NOT NULL,
    company_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_buses_plate (plate_number),
    CONSTRAINT fk_buses_company
        FOREIGN KEY (company_id) REFERENCES companies (id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS routes (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    number VARCHAR(10) NOT NULL,
    title VARCHAR(120) NOT NULL,
    distance_km INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_routes_number (number)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS drivers (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    full_name VARCHAR(120) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    license_number VARCHAR(20) NOT NULL,
    company_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_drivers_license (license_number),
    CONSTRAINT fk_drivers_company
        FOREIGN KEY (company_id) REFERENCES companies (id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS driver_routes (
    driver_id INT UNSIGNED NOT NULL,
    route_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (driver_id, route_id),
    CONSTRAINT fk_driver_routes_driver
        FOREIGN KEY (driver_id) REFERENCES drivers (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_driver_routes_route
        FOREIGN KEY (route_id) REFERENCES routes (id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;
