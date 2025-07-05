dependencies = ["20250703222105_create_rules_collection"]

def upgrade(db):
    db.create_collection("customers")
    db.customers.create_index("name", unique=True)

    # Optionally add validation rules (MongoDB >= 3.6)
    db.command("collMod", "customers", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "request_rate_limit"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "request_rate_limit": {
                    "bsonType": "int",
                    "minimum": 1,
                    "description": "must be a positive integer"
                }
            }
        }
    })

def downgrade(db):
    db.drop_collection("customers")

def comment(self):
    return 'Creating customers collection'