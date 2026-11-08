# CleanQ validation tests

Each rule is checked in layers: the browser helps honest users, Flask is the real gatekeeper, and the database is the last line of defense. Ticket count before and after all Flask tests: <number> and <same number>.

| Rule | Layer | How I tested it | What happened |
|------|-------|-----------------|---------------|
| Name is at most 60 characters | Browser | Typed more than 60 characters in the name field on New Order | The field stops accepting characters at 60 (`maxlength="60"`) |
| Name, mobile number, service and kilos are required | Flask | `curl.exe -i -X POST .../join -d "name=" -d "phone=not-a-number" -d "service_id=999" -d "kilos=abc"` | 400 BAD REQUEST, nothing saved |
| Name is at most 60 characters | Flask | `curl.exe` with a 200-character name | 400 BAD REQUEST, nothing saved |
| Kilos are between 0.1 and 50 | Flask | `curl.exe` with `kilos=500` | 400 BAD REQUEST, nothing saved |
| Kilos must be a real number | Flask | `curl.exe` with `kilos=NaN` | 400 BAD REQUEST, nothing saved |
| A switched-off service cannot be chosen | Flask | Switched a service off in Manage services, then `curl.exe` with its `service_id` | 400 BAD REQUEST, nothing saved |
| A ticket needs a service that exists | Database (FOREIGN KEY) | `INSERT INTO tickets (customer_id, service_id, kilos, price_per_kilo) VALUES (1, 999, 2, 35);` in psql | ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey" |
| Status must be an allowed stage | Database (CHECK) | `UPDATE tickets SET status = 'lost' WHERE id = 1;` | ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status" |
| A claimed ticket needs a claim time | Database (CHECK) | `UPDATE tickets SET status = 'claimed' WHERE id = 1;` | ERROR: new row for relation "tickets" violates check constraint "ck_tickets_claimed_has_time" |
| Kilos are between 0.1 and 50 | Database (CHECK) | `UPDATE tickets SET kilos = 500 WHERE id = 1;` | ERROR: new row for relation "tickets" violates check constraint "ck_tickets_kilos" |
| Turnaround is more than 0 hours | Database (CHECK) | `INSERT INTO services (name, price_per_kilo, hours) VALUES ('Test', 10, 0);` | ERROR: new row for relation "services" violates check constraint "ck_services_hours" |
| One customer per mobile number | Database (UNIQUE) | `INSERT INTO customers (name, phone) VALUES ('Copy', '09171234567');` | ERROR: duplicate key value violates unique constraint "customers_phone_key" |
| A customer must have a name | Database (NOT NULL) | `INSERT INTO customers (name, phone) VALUES (NULL, '09170000000');` | ERROR: null value in column "name" of relation "customers" violates not-null constraint |
| Names are at most 60 characters | Database (column length) | `INSERT INTO customers (name, phone) VALUES (repeat('a', 61), '09170000001');` | ERROR: value too long for type character varying(60) |
| A service with tickets cannot be deleted | Database (RESTRICT) | `DELETE FROM services WHERE id = 1;` | ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets" |

**Good row:** `INSERT INTO tickets (customer_id, service_id, kilos, price_per_kilo) VALUES (1, 1, 2, 65) RETURNING id, status, paid, created_at;` returned status `received`, paid `f` and a `created_at` filled in by the database. I deleted the test row afterwards.

**No SQL in f-strings:** `Select-String -Path app.py,models.py -CaseSensitive -Pattern 'f["''].*(SELECT|INSERT|UPDATE|DELETE)'` printed nothing. All queries use SQLAlchemy, which sends values separately from the SQL.