import sqlite3
import random
from datetime import datetime, timedelta




def seed_data_load(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ---------------------------------------------------
    # HELPERS
    # ---------------------------------------------------

    def random_date():
        start_date = datetime(2026, 1, 1)
        end_date = datetime(2026, 5, 1)

        delta = end_date - start_date
        random_days = random.randint(0, delta.days)

        return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")


    # ---------------------------------------------------
    # ADDRESS DATA
    # ---------------------------------------------------

    addresses = [
        ("Plot 11 Industrial Area", "", "Bangalore", "Karnataka", "India", "560001"),
        ("Plot 22 Manufacturing Zone", "", "Hyderabad", "Telangana", "India", "500001"),
        ("Sector 5 Export Hub", "", "Pune", "Maharashtra", "India", "411001"),
        ("Logistics Park Road", "", "Chennai", "Tamil Nadu", "India", "600001"),
        ("Warehouse Street 1", "", "Mumbai", "Maharashtra", "India", "400001"),
        ("Transport Nagar", "", "Delhi", "Delhi", "India", "110001"),
        ("Dockyard Main Road", "", "Kolkata", "West Bengal", "India", "700001"),
        ("Industrial Layout", "", "Ahmedabad", "Gujarat", "India", "380001")
    ]

    address_ids = []

    for addr in addresses:
        cursor.execute("""
        INSERT INTO address_master (
            address_line_1,
            address_line_2,
            city,
            state,
            country,
            postal_code
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, addr)

        address_ids.append(cursor.lastrowid)

    # ---------------------------------------------------
    # PLANTS
    # ---------------------------------------------------

    plants = [
        ("PLT001", "Bangalore Manufacturing Plant", address_ids[0]),
        ("PLT002", "Hyderabad Steel Plant", address_ids[1]),
        ("PLT003", "Pune Processing Unit", address_ids[2]),
        ("PLT004", "Chennai Packaging Unit", address_ids[3]),
    ]

    plant_ids = []

    for plant in plants:
        cursor.execute("""
        INSERT INTO plant_master (
            plant_code,
            plant_name,
            address_id
        )
        VALUES (?, ?, ?)
        """, plant)

        plant_ids.append(cursor.lastrowid)

    # ---------------------------------------------------
    # DESTINATIONS
    # ---------------------------------------------------

    destinations = [
        ("DST001", "Mumbai Central Warehouse", address_ids[4]),
        ("DST002", "Delhi Distribution Center", address_ids[5]),
        ("DST003", "Kolkata Regional Hub", address_ids[6]),
        ("DST004", "Ahmedabad Depot", address_ids[7]),
    ]

    destination_ids = []

    for dest in destinations:
        cursor.execute("""
        INSERT INTO destination_master (
            destination_code,
            destination_name,
            address_id
        )
        VALUES (?, ?, ?)
        """, dest)

        destination_ids.append(cursor.lastrowid)

    # ---------------------------------------------------
    # MATERIALS
    # ---------------------------------------------------

    materials = [
        ("MAT001", "Steel Rod", "KG", "Raw Material", 2.5),
        ("MAT002", "Copper Wire", "KG", "Raw Material", 1.2),
        ("MAT003", "Plastic Granules", "KG", "Polymer", 0.8),
        ("MAT004", "Aluminium Sheet", "KG", "Metal", 3.1),
        ("MAT005", "Rubber Seal", "PCS", "Component", 0.2),
        ("MAT006", "Machine Bolt", "PCS", "Hardware", 0.05),
        ("MAT007", "Industrial Paint", "LTR", "Chemical", 1.0),
        ("MAT008", "Steel Pipe", "MTR", "Raw Material", 4.5),
        ("MAT009", "Hydraulic Valve", "PCS", "Equipment", 1.8),
        ("MAT010", "Electric Motor", "PCS", "Equipment", 15.0),
        ("MAT011", "Packing Box", "PCS", "Packaging", 0.3),
        ("MAT012", "PVC Sheet", "SQM", "Polymer", 2.0),
        ("MAT013", "Bearing Unit", "PCS", "Component", 0.7),
        ("MAT014", "Lubricant Oil", "LTR", "Chemical", 0.9),
        ("MAT015", "Control Panel", "PCS", "Electrical", 12.0),
        ("MAT016", "Transformer Coil", "PCS", "Electrical", 8.5),
        ("MAT017", "Glass Fiber Roll", "MTR", "Insulation", 1.4),
        ("MAT018", "Foam Padding", "PCS", "Packaging", 0.4),
        ("MAT019", "Industrial Fan", "PCS", "Equipment", 7.2),
        ("MAT020", "Conveyor Belt", "MTR", "Mechanical", 6.0),
        ("MAT021", "Sensor Module", "PCS", "Electronics", 0.15),
        ("MAT022", "Circuit Board", "PCS", "Electronics", 0.25),
        ("MAT023", "LED Indicator", "PCS", "Electronics", 0.05),
        ("MAT024", "Cooling Pipe", "MTR", "Mechanical", 2.2),
        ("MAT025", "Valve Cap", "PCS", "Component", 0.08),
    ]

    material_ids = []

    for material in materials:
        cursor.execute("""
        INSERT INTO material_master (
            material_code,
            material_description,
            uom,
            material_type,
            weight_per_unit
        )
        VALUES (?, ?, ?, ?, ?)
        """, material)

        material_ids.append(cursor.lastrowid)

    # ---------------------------------------------------
    # SHIPMENTS
    # ---------------------------------------------------

    shipment_ids = []

    for i in range(1, 16):

        shipment_number = f"SHIP{1000 + i}"

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
            shipment_number,
            random.choice(plant_ids),
            random.choice(destination_ids),
            f"KA{random.randint(1,99):02d}AB{random.randint(1000,9999)}",
            random.choice([
                "ABC Logistics",
                "FastTrack Transport",
                "BlueLine Movers",
                "National Freight",
                "Speed Cargo"
            ]),
            random_date()
        ))

        shipment_ids.append(cursor.lastrowid)

    # ---------------------------------------------------
    # DELIVERIES
    # ---------------------------------------------------

    delivery_ids = []

    delivery_counter = 1

    for shipment_id in shipment_ids:

        num_deliveries = random.randint(1, 3)

        for _ in range(num_deliveries):

            delivery_number = f"DEL{1000 + delivery_counter}"

            cursor.execute("""
            INSERT INTO delivery (
                delivery_number,
                shipment_id,
                delivery_date,
                invoice_number
            )
            VALUES (?, ?, ?, ?)
            """, (
                delivery_number,
                shipment_id,
                random_date(),
                f"INV{2000 + delivery_counter}"
            ))

            delivery_ids.append(cursor.lastrowid)

            delivery_counter += 1

    # ---------------------------------------------------
    # DELIVERY LINE ITEMS
    # ---------------------------------------------------

    for delivery_id in delivery_ids:

        num_items = random.randint(2, 6)

        selected_materials = random.sample(material_ids, num_items)

        for material_id in selected_materials:

            quantity = round(random.uniform(10, 500), 2)

            uom = cursor.execute("""
            SELECT uom
            FROM material_master
            WHERE material_id = ?
            """, (material_id,)).fetchone()[0]

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
                quantity,
                uom,
                f"BATCH{random.randint(10000,99999)}"
            ))

    # ---------------------------------------------------
    # SAVE
    # ---------------------------------------------------

    conn.commit()

    # ---------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------

    print("Seed data inserted successfully!")

    for table in [
        "address_master",
        "plant_master",
        "destination_master",
        "material_master",
        "shipment",
        "delivery",
        "delivery_line_item"
    ]:

        count = cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {count}")

    conn.close()