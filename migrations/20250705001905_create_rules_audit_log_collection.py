dependencies = ["20250705001339_create_customers_collection"]

def upgrade(db):
    db.create_collection("rule_audit_logs")
    db.rule_audit_logs.create_index("customer_id")
    db.rule_audit_logs.create_index("rule_id")
    db.rule_audit_logs.create_index("operation")

    db.command({
        "collMod": "rule_audit_logs",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["customer_id", "user", "operation", "timestamp"],
                "properties": {
                    "customer_id": {"bsonType": "objectId"},
                    "user": {"bsonType": "string"},
                    "operation": {
                        "enum": ["create", "update", "delete"],
                        "description": "Type of change"
                    },
                    "timestamp": {"bsonType": "date"},
                    "rule_id": {
                        "bsonType": ["objectId", "null"],
                        "description": "Optional rule ID"
                    },
                    "body": {
                        "bsonType": ["object", "null"],
                        "description": "Optional request body snapshot"
                    },
                }
            }
        },
        "validationLevel": "moderate"
    })

def downgrade(db):
    db.drop_collection("rule_audit_logs")

def comment(self):
    return 'Creating rules audit log collection'
    