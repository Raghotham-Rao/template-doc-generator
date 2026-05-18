import sqlite3
from pathlib import Path

# ---------------------------------------------------
# DATABASE SETUP
# ---------------------------------------------------

DB_PATH = "transport_doc_generator.db"

# Remove old DB if needed during development
# Path(DB_PATH).unlink(missing_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")


# ---------------------------------------------------
# ADDRESS MASTER
# ---------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS address_master (
    address_id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_line_1 TEXT,
    address_line_2 TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    postal_code TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")


# ---------------------------------------------------
# PLANT MASTER
# ---------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS plant_master (
    plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_code TEXT UNIQUE NOT NULL,
    plant_name TEXT NOT NULL,
    address_id INTEGER,

    FOREIGN KEY (address_id)
        REFERENCES address_master(address_id)
);
""")


# ---------------------------------------------------
# DESTINATION MASTER
# ---------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS destination_master (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_code TEXT UNIQUE NOT NULL,
    destination_name TEXT NOT NULL,
    address_id INTEGER,

    FOREIGN KEY (address_id)
        REFERENCES address_master(address_id)
);
""")


# ---------------------------------------------------
# MATERIAL MASTER
# ---------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS material_master (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_code TEXT UNIQUE NOT NULL,
    material_description TEXT,
    uom TEXT,
    material_type TEXT,
    weight_per_unit REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")


# ---------------------------------------------------
# SHIPMENT
# ---------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS shipment (
    shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_number TEXT UNIQUE NOT NULL,

    plant_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,

    vehicle_number TEXT,
    transporter_name TEXT,
    shipment_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (plant_id)
        REFERENCES plant_master(plant_id),

    FOREIGN KEY (destination_id)
        REFERENCES destination_master(destination_id)
);
""")


# ---------------------------------------------------
# DELIVERY
# ---------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS delivery (
    delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_number TEXT UNIQUE NOT NULL,

    shipment_id INTEGER NOT NULL,

    delivery_date DATE,
    invoice_number TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (shipment_id)
        REFERENCES shipment(shipment_id)
);
""")


# ---------------------------------------------------
# DELIVERY LINE ITEM
# ---------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS delivery_line_item (
    line_item_id INTEGER PRIMARY KEY AUTOINCREMENT,

    delivery_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,

    quantity REAL,
    uom TEXT,

    batch_number TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (delivery_id)
        REFERENCES delivery(delivery_id),

    FOREIGN KEY (material_id)
        REFERENCES material_master(material_id)
);
""")


# ---------------------------------------------------
# DOCUMENT TEMPLATE
# ---------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS document_template (
    template_id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name TEXT NOT NULL,
    html_template TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")


# ---------------------------------------------------
# TEMPLATE VARIABLE MAPPING
# ---------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS template_variable_mapping (
    mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,

    template_id INTEGER NOT NULL,

    variable_name TEXT NOT NULL,

    source_table TEXT NOT NULL,
    source_column TEXT NOT NULL,

    FOREIGN KEY (template_id)
        REFERENCES document_template(template_id)
);
""")


# ---------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------

# Address
cursor.execute("""
INSERT INTO address_master (
    address_line_1,
    city,
    state,
    country,
    postal_code
)
VALUES (?, ?, ?, ?, ?)
""", (
    "Plot 21 Industrial Area",
    "Bangalore",
    "Karnataka",
    "India",
    "560001"
))

address_id = cursor.lastrowid


# Plant
cursor.execute("""
INSERT INTO plant_master (
    plant_code,
    plant_name,
    address_id
)
VALUES (?, ?, ?)
""", (
    "PLT001",
    "Bangalore Plant",
    address_id
))

plant_id = cursor.lastrowid


# Destination
cursor.execute("""
INSERT INTO destination_master (
    destination_code,
    destination_name,
    address_id
)
VALUES (?, ?, ?)
""", (
    "DST001",
    "Chennai Warehouse",
    address_id
))

destination_id = cursor.lastrowid


# Material
cursor.execute("""
INSERT INTO material_master (
    material_code,
    material_description,
    uom,
    material_type,
    weight_per_unit
)
VALUES (?, ?, ?, ?, ?)
""", (
    "MAT001",
    "Steel Rod",
    "KG",
    "Raw Material",
    2.5
))

material_id = cursor.lastrowid


# Shipment
cursor.execute("""
INSERT INTO shipment (
    shipment_number,
    plant_id,
    destination_id,
    vehicle_number,
    transporter_name,
    shipment_date
)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    "SHIP001",
    plant_id,
    destination_id,
    "KA01AB1234",
    "ABC Logistics",
    "2026-05-16"
))

shipment_id = cursor.lastrowid


# Delivery
cursor.execute("""
INSERT INTO delivery (
    delivery_number,
    shipment_id,
    delivery_date,
    invoice_number
)
VALUES (?, ?, ?, ?)
""", (
    "DEL001",
    shipment_id,
    "2026-05-16",
    "INV001"
))

delivery_id = cursor.lastrowid


# Delivery Line Item
cursor.execute("""
INSERT INTO delivery_line_item (
    delivery_id,
    material_id,
    quantity,
    uom,
    batch_number
)
VALUES (?, ?, ?, ?, ?)
""", (
    delivery_id,
    material_id,
    100,
    "KG",
    "BATCH001"
))


# ---------------------------------------------------
# SAVE
# ---------------------------------------------------

conn.commit()

print("Database setup completed successfully!")

# ---------------------------------------------------
# VERIFY DATA
# ---------------------------------------------------

query = """
SELECT
    s.shipment_number,
    d.delivery_number,
    m.material_description,
    li.quantity
FROM shipment s
JOIN delivery d
    ON s.shipment_id = d.shipment_id
JOIN delivery_line_item li
    ON d.delivery_id = li.delivery_id
JOIN material_master m
    ON li.material_id = m.material_id;
"""

rows = cursor.execute(query).fetchall()

print("\nSample Data:")
for row in rows:
    print(row)

conn.close()