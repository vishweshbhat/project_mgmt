CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,  -- Adding the description column
    status INT NOT NULL,
    storage_location VARCHAR(255) NOT NULL
);
