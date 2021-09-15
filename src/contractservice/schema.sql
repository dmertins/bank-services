DROP TABLE IF EXISTS contract;

CREATE TABLE contract (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    debt REAL NOT NULL,
    is_open BOOLEAN NOT NULL,
    closed_on DATETIME
);
