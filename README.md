# Linux Permission Auditor

A security toolkit combining Linux system administration, Python-based permission analysis, and SQL-based audit tracking to identify and trace permission misconfigurations, following the principle of least privilege.

## Part 1: Linux Permission Auditing

Used `ls -l` to inspect real file and directory permissions on the system, reading the `user/group/other` structure (e.g., `drwxr-xr-x`, `-rw-rw-r--`).

### Security Test
Ran `chmod 777 subnet_calc.py` to intentionally create a worst-case permission setting (`rwxrwxrwx`) and observed the result with `ls -l`. This demonstrated the risk directly: granting "other" (every other user on the system) both write and execute access means any other user could modify the file's contents or run it directly — a clear violation of the principle of least privilege.

### Fix
Ran `chmod 644 subnet_calc.py` to restore a secure, appropriate setting (`rw-r--r--`) — allowing the owner to read/write, while everyone else can only read.

This exercise established the core security concept the rest of the project builds on: permissions should always be scoped to the minimum access necessary, not left wide open by default.

## Part 2: Python Permission-to-Octal Converter

Built `permission_auditor.py`, which converts a raw Linux permission string (like `rwxr-xr--`) into its octal representation (like `754`) — the same numeric format used by `chmod`.

### Functions

- **`chunk_to_value(chunk)`** — takes a 3-character permission chunk (e.g., `rwx`, `r-x`, `r--`) and returns its point total using the same values `chmod` uses internally: read = 4, write = 2, execute = 1.

- **`permission_to_octal(perm_string)`** — takes a full 9-character permission string, slices it into user/group/other chunks, runs each through `chunk_to_value`, and combines the three results into the final octal string (e.g., `"rwxr-xr--"` → `"754"`).

### Risk Flagging
Within `permission_to_octal`, the function checks whether "other" has write or execute access — the two permissions most likely to violate the principle of least privilege — and prints a warning if either is found:

WARNING: OTHER GROUP HAS EXCESSIVE PERMISSIONS

This connects directly to the Part 1 findings: instead of manually running `chmod` and eyeballing `ls -l` output, this script automates the detection of overly permissive files.

## Part 3: SQL Database — Systems, Owners, and Risk Detection

Built a SQLite database (`systems.db`) with two tables to track devices and their owners:

- **systems** — `device_id` (primary key), `hostname`, `permission_string`
- **owners** — `device_id` (primary key), `employee_name`

### Risk-Detection Queries
Used the `LIKE` operator with `%` wildcards to detect risky permission patterns:
- `LIKE '%rwx'` — finds systems where "other" has full read/write/execute access
- `LIKE '%w_'` — finds systems where "other" has write access, regardless of the execute bit

### Combined Join + Risk Query
Used a `LEFT JOIN` to connect `systems` and `owners` on `device_id`, then filtered with `WHERE permission_string LIKE '%w_'` to answer a real audit question: which employee owns a system with a risky, world-writable permission setting?

```sql
SELECT * FROM systems 
LEFT JOIN owners ON systems.device_id = owners.device_id 
WHERE permission_string LIKE '%w_';
```

This ties the whole project together: Linux permission auditing → Python-based octal conversion and risk flagging → SQL-based tracking of which system belongs to which employee, so risky configurations can be traced back to a responsible party.
