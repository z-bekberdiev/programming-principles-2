# TSIS 1: PhoneBook — Extended Contact Management

## 1. Objective

The goal is to extend the "PhoneBook" application from Practice 7-8 with an enriched data model, advanced terminal interactions and a new "PostgreSQL" database-side logic as well as to go beyond the basic CRUD operations and stored procedures by introducing a relational schema design, multi-field search and file-based data exchange.

---

## 2. Base

| Done In      | Feature                                               |  
|:------------:|-------------------------------------------------------|
| `Practice 7` | Basic CRUD operations using `psycopg2` module         |
| `Practice 7` | Import data from `CSV` file / Enter data via terminal |
| `Practice 7` | Query by name / phone                                 |
| `Practice 8` | Pattern-based search function by name / phone         |
| `Practice 8` | `Upsert` procedure / Bulk-insert with validation      |
| `Practice 8` | Paginated query function (LIMIT / OFFSET)             |
| `Practice 8` | `Delete` procedure by name / phone                    |

---

## 3. Tasks

### 3.1. Extended Contact Management

Update the database schema to support richer contact data:

1. **Multiple phone numbers per contact** — create a separate `phones` table with a foreign key to `contacts` (one-to-many). Each phone has a `phone_type`: `Home`, `Work` or `Mobile`.
2. **Email** — add an `email_address` field to the `contacts` table.
3. **Birthday** — add a `birthday_date` field of a type `DATE` to the `contacts` table.
4. **Group** — create a `groups` table (`Family`, `Colleagues`, `Friends` or `Other`) and link each contact to a `group_name` using a foreign key.

---

### 3.2. Advanced Terminal Search & Filter

Extend the terminal interface to support:

1. **Filter by group** — show only contacts belonging to a selected category.
2. **Search by email** — implement a partial match.
3. **Sorted result** — allow the user to sort the output by first / last name or birthday date.
4. **Paginated navigation** — build a terminal loop that lets the user navigate pages with `previous`, `next` and `quit`.

---

### 3.3. Import / Export

1. **Export to JSON** — write all contacts (including phones and groups) to a `JSON` file.
2. **Import from JSON** — read contacts from a `JSON` file and insert them into the DB. On duplicate (same name), ask the user to skip or overwrite.
3. **Extend CSV import** — update the existing CSV importer to handle the new fields (`phone_type`, `email_address`, `birthday_date` and `group_name`).

---

### 3.4. New Stored Procedures (PL/pgSQL)

Add the following server-side objects:

1. **Procedure** `attach_phone_to_contact(contact_id VARCHAR, phone_number VARCHAR, phone_type VARCHAR)` — adds a new phone number to an existing contact.
2. **Procedure** `relocate_contact_to_group(contact_id VARCHAR, group_name VARCHAR)` — moves a contact to a different group, otherwise creates the new group.
3. **Function** `search_contact(search_pattern VARCHAR, search_column VARCHAR)` — extends the pattern-based search to match against `email_address` and all `phone_number` / `phone_type` in the `phones` table, since the schema now has multiple phones in the separate table.

---

### 3.5. Save to GitHub

Example repository structure:

```
tsis-1/
├── README.md
├── phonebook.py
└── assets/
    ├── credentials.ini
    ├── contacts.csv
    ├── contacts.json
    ├── schemas.sql
    ├── functions.sql
    └── procedures.sql
```
