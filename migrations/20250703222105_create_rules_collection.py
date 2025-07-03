
dependencies = []

def upgrade(db):
        if "rules" not in db.list_collection_names():
            db.create_collection("rules")

        print("Creating JSON schema validator for 'rules' collection...")

        rules_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["name", "description", "ip", "customer_id"],
                "properties": {
                    "name": {
                        "bsonType": "string",
                        "description": "Rule name (must be unique)"
                    },
                    "description": {
                        "bsonType": "string",
                        "description": "Free-text description"
                    },
                    "ip": {
                        "bsonType": "string",
                        "description": "IP address string"
                    },
                    "expired_date": {
                        "bsonType": ["date", "null"],
                        "description": "Optional expiration date (ISO format)"
                    },
                    "customer_id": {
                        "bsonType": "int",
                        "description": "Integer referring to a customer"
                    }
                }
            }
        }

        # Apply schema validation
        db.command({
            "collMod": "rules",
            "validator": rules_validator,
            "validationLevel": "moderate"
        })

        # Add unique index to 'name'
        db.rules.create_index("name", unique=True)
        print("✅ Migration '0001_create_rules' applied.")

def downgrade(db):
    db.drop_collection("rules")
    print("⛔ Migration '0001_create_rules' reverted.")

def comment(self):
    return 'Creating Rules Collection'
    