CREATE TABLE application (
  id SERIAL PRIMARY KEY,
  name VARCHAR(80) NOT NULL UNIQUE,
  display_name VARCHAR(80) NOT NULL
);
