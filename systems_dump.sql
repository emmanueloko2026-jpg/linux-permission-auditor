PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE systems (
    device_id INTEGER PRIMARY KEY,
    hostname TEXT,
    permission_string TEXT
);
INSERT INTO systems VALUES(1,'WebServer01','rwxr-xr--');
INSERT INTO systems VALUES(2,'DBServer02','rwxrwxrwx');
INSERT INTO systems VALUES(3,'FileShare03','rw-r--r--');
INSERT INTO systems VALUES(4,'AdminPC04','rwxrwxr-x');
CREATE TABLE owners(device_id INTEGER PRIMARY KEY, employee_name TEXT);
INSERT INTO owners VALUES(1,'Marco');
INSERT INTO owners VALUES(2,'Sophia');
INSERT INTO owners VALUES(3,'Chloe');
INSERT INTO owners VALUES(4,'Amanda');
COMMIT;
