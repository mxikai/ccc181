# CleanQ schema review

I checked the schema against six questions: coverage, one fact in one place, facts not results, bad data, deletes and types. Every Stores data = Yes requirement and every top task in my personas has a table or column, so there are no missing columns. The entries below are the problems and strengths I found.

## Entry 1: ticket price and status

**Works well:** `tickets.price_per_kilo` stores the price at the time of the order, and the total is computed from kilos × price instead of stored. When staff change a service's price (FR-12), old tickets and "Claimed today" sales do not change, and no total ever has to be rewritten. This came from the "Facts, not results" and "One fact in one place" questions.

**Problem:** The `status` column and the `ready_at` and `claimed_at` columns can disagree. A ticket could be `claimed` with no `claimed_at`, which would leave it out of "Claimed today" (FR-11), or have a `claimed_at` earlier than its `created_at`. The column constraints alone do not stop this. Found with question 4, Bad data.

**Change:** Added three table-level CHECK constraints to `tickets` in `schema.md` (section 2c):
- `CHECK (status <> 'claimed' OR claimed_at IS NOT NULL)`
- `CHECK (status NOT IN ('ready', 'claimed') OR ready_at IS NOT NULL)`
- `CHECK (claimed_at IS NULL OR claimed_at >= created_at)`

The ERD is unchanged because no columns were added.

## Entry 2: deletes and unused columns

**Works well:** Both `tickets.customer_id` and `tickets.service_id` use RESTRICT, and services have an `is_active` flag. Staff can switch a service off, but a service or customer with tickets can never be deleted, so old tickets and sales records stay. Only `tickets.created_by` uses SET NULL, because losing "who logged it" matters less than losing the ticket. This came from question 5, Deletes.

**Problem:** `customers.created_at` and `staff.created_at` are not needed by any requirement. Nothing in the app shows or uses when a customer or staff account was made. Found with question 1, Coverage.

**Change:** Removed `created_at` from `customers` and `staff` in `schema.md` (sections 2b and 2c) and in the ERD. `timestamptz` is still used in `tickets`, so every required constraint type is still in the schema.

## Entry 3: customers and bad data

**Works well:** Name and mobile number are stored once in `customers`, not on every ticket. The phone column is UNIQUE with a CHECK for a valid PH number, so one person cannot become two customers by typing the number in different formats once the app normalizes it. Before this, Ana Reyes was stored twice in the list of tickets. This came from question 2, One fact in one place.

**Problem:** The database cannot stop two kinds of mistakes. A foreign key only checks that a service exists, so a ticket can still be created for a service that was switched off. A double tap on "Create ticket" can also make two identical tickets. Found with question 4, Bad data.

**Change:** Kept the schema as it is. The New Order form will only list services where `is_active` is true, and the double-submit guard in `main.js` stays. A database rule for either one would need extra columns or triggers that go beyond a laundry shop's needs, so I am handling them in the app and will test both in Part 4.

## Entry 4: types and estimated pickup

**Works well:** Every moment in time is `timestamptz`, money is `numeric` rather than float or text, kilos have a range CHECK, and `paid` is a boolean. Mobile numbers are text because they are identifiers and not numbers to calculate with. This came from question 6, Types.

**Problem:** Estimated pickup is computed as `tickets.created_at` plus the current `services.hours`. If staff change a service's turnaround (FR-12), the estimate shown on existing tickets changes too. Found with question 3, Facts not results.

**Change:** Kept it, with no stored estimate or `hours` copy on `tickets`. An estimated pickup is a guess that should follow the shop's current turnaround, unlike a price, which is a record of what was charged. Storing a copy would add a column that goes out of date and has to be kept in sync.