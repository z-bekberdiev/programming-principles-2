# TSIS 1: PhoneBook — Extended Contact Management

## 1. Objective

The goal is to extend the "PhoneBook" application from Practice 7-8 with an enriched data model, advanced terminal interactions and new "PostgreSQL" database-side logic as well as to go beyond basic CRUD and stored procedures by introducing a relational schema design, multi-field search and file-based data exchange.

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

### 3.1 Extended Contact Management

Update the database schema to support richer contact data:

1. **Multiple phone numbers per contact** — create a separate `phones` table with a foreign key to `contacts` (one-to-many). Each phone has a type: `home`, `work` or `mobile`.
2. **Email address** — add an `email` field to the `contacts` table.
3. **Birthday** — add a `birthday` field of a type `DATE` to the `contacts` table.
4. **Contact group/category** — create a `groups` table (`family`, `work`, `friend` or `other`) and link each contact to a group using a foreign key.

---

### 3.2 Advanced Terminal Search & Filter

Extend the terminal interface to support:

1. **Filter by group** — show only contacts belonging to a selected category.
2. **Search by email** — implement a partial match.
3. **Sort results** — allow the user to sort the output by name, birthday or date added.
4. **Paginated navigation** — build a terminal loop that lets the user navigate pages with `previous`, `next` and `quit`.

---

### 3.3 Import / Export

1. **Export to JSON** — write all contacts (including phones and groups) to a `JSON` file.
2. **Import from JSON** — read contacts from a `JSON` file and insert them into the DB. On duplicate (same name), ask the user to skip or overwrite.
3. **Extend CSV import** — update the existing CSV importer to handle the new fields (`type`, `email`, `birthday` and `group`).

---

### 3.4 New Stored Procedures (PL/pgSQL)

Add the following server-side objects:

1. **Procedure** `addPhoneToContact(contactName VARCHAR, phoneNumber VARCHAR, phoneType VARCHAR)` — adds a new phone number to an existing contact.
2. **Procedure** `moveContactToGroup(contactName VARCHAR, groupType VARCHAR)` — moves a contact to a different group, otherwise creates the new group.
3. **Function** `searchByPattern(patternQuery TEXT)` — extends the pattern-based search to match against `email` and all phones in the `phones` table, since the schema now has multiple phones in the separate table.

---

### 3.5 Save to GitHub

Example repository structure:

```
tsis-1/
├── phonebook.py
├── frontend.py
├── backend.py
├── credentials.ini
├── schema.sql
├── functions.sql
├── procedures.sql
├── contacts.csv
└── README.md
```
