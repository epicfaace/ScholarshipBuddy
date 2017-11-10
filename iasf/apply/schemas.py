class JSONListFieldSchemas:
    """
    Schemas for all the JSON List Fields.
    Each key represents the field name.
    """
    schema = {
        "scores_ap": {
            "$schema": "http://json-schema.org/draft-06/schema#",
            "title": "AP Scores",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "exam": {
                        "type": "string",
                        "title": "Exam"
                    },
                    "score": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5,
                        "title": "Score"
                    }
                },
                "required": [
                    "exam",
                    "score"
                ],
                "order": [
                    "exam",
                    "score"
                ]
            }
        },
        "activities": {
            "type": "array",
            "items":
                {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "title": "Name"
                        },
                        "grade": {
                            "type": "string",
                            "title": "Grades Participated"
                        },
                        "description": {
                            "type": "string",
                            "title": "Description",
                            "format": "textarea"
                        }
                    },
                    "order": [
                        "name", "grade", "description"
                    ]
                }
        }
    }