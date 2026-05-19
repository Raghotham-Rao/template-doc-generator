import sqlite3
from pathlib import Path

# ---------------------------------------------------
# DATABASE SETUP
# ---------------------------------------------------

def database_setup(DB_PATH):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
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