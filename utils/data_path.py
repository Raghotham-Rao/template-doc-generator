# nodes.py

nodes = [
    {
        "label": "shipment",
        "value": "shipment",
        "children": [
            {
                "label": "shipment_id",
                "value": "shipment.shipment_id"
            },
            {
                "label": "shipment_number",
                "value": "shipment.shipment_number"
            },
            {
                "label": "vehicle_number",
                "value": "shipment.vehicle_number"
            },
            {
                "label": "transporter_name",
                "value": "shipment.transporter_name"
            },
            {
                "label": "shipment_date",
                "value": "shipment.shipment_date"
            },

            # ----------------------------------------
            # PLANT
            # ----------------------------------------

            {
                "label": "plant",
                "value": "plant",
                "children": [
                    {
                        "label": "plant_id",
                        "value": "plant.plant_id"
                    },
                    {
                        "label": "plant_code",
                        "value": "plant.plant_code"
                    },
                    {
                        "label": "plant_name",
                        "value": "plant.plant_name"
                    },

                    {
                        "label": "address",
                        "value": "plant.address",
                        "children": [
                            {
                                "label": "address_line_1",
                                "value": "plant.address.address_line_1"
                            },
                            {
                                "label": "address_line_2",
                                "value": "plant.address.address_line_2"
                            },
                            {
                                "label": "city",
                                "value": "plant.address.city"
                            },
                            {
                                "label": "state",
                                "value": "plant.address.state"
                            },
                            {
                                "label": "country",
                                "value": "plant.address.country"
                            },
                            {
                                "label": "postal_code",
                                "value": "plant.address.postal_code"
                            }
                        ]
                    }
                ]
            },

            # ----------------------------------------
            # DESTINATION
            # ----------------------------------------

            {
                "label": "destination",
                "value": "destination",
                "children": [
                    {
                        "label": "destination_id",
                        "value": "destination.destination_id"
                    },
                    {
                        "label": "destination_code",
                        "value": "destination.destination_code"
                    },
                    {
                        "label": "destination_name",
                        "value": "destination.destination_name"
                    },

                    {
                        "label": "address",
                        "value": "destination.address",
                        "children": [
                            {
                                "label": "address_line_1",
                                "value": "destination.address.address_line_1"
                            },
                            {
                                "label": "address_line_2",
                                "value": "destination.address.address_line_2"
                            },
                            {
                                "label": "city",
                                "value": "destination.address.city"
                            },
                            {
                                "label": "state",
                                "value": "destination.address.state"
                            },
                            {
                                "label": "country",
                                "value": "destination.address.country"
                            },
                            {
                                "label": "postal_code",
                                "value": "destination.address.postal_code"
                            }
                        ]
                    }
                ]
            },

            # ----------------------------------------
            # DELIVERIES
            # ----------------------------------------

            {
                "label": "deliveries",
                "value": "deliveries",
                "children": [
                    {
                        "label": "delivery_id",
                        "value": "deliveries.delivery_id"
                    },
                    {
                        "label": "delivery_number",
                        "value": "deliveries.delivery_number"
                    },
                    {
                        "label": "delivery_date",
                        "value": "deliveries.delivery_date"
                    },
                    {
                        "label": "invoice_number",
                        "value": "deliveries.invoice_number"
                    },

                    # --------------------------------
                    # LINE ITEMS
                    # --------------------------------

                    {
                        "label": "line_items",
                        "value": "deliveries.line_items",
                        "children": [
                            {
                                "label": "quantity",
                                "value": "deliveries.line_items.quantity"
                            },
                            {
                                "label": "uom",
                                "value": "deliveries.line_items.uom"
                            },
                            {
                                "label": "batch_number",
                                "value": "deliveries.line_items.batch_number"
                            },

                            # ------------------------
                            # MATERIAL
                            # ------------------------

                            {
                                "label": "material",
                                "value": "deliveries.line_items.material",
                                "children": [
                                    {
                                        "label": "material_code",
                                        "value": "deliveries.line_items.material.material_code"
                                    },
                                    {
                                        "label": "material_description",
                                        "value": "deliveries.line_items.material.material_description"
                                    },
                                    {
                                        "label": "material_type",
                                        "value": "deliveries.line_items.material.material_type"
                                    },
                                    {
                                        "label": "weight_per_unit",
                                        "value": "deliveries.line_items.material.weight_per_unit"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
]