from decimal import Decimal
from django.db import models


def serialize_for_audit(data):
    """Convert Decimal, Django models, and other non-serializable types to JSON-friendly formats"""
    if isinstance(data, dict):
        return {k: serialize_for_audit(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [serialize_for_audit(item) for item in data]
    elif isinstance(data, Decimal):
        return float(data)
    elif isinstance(data, models.Model):
        # Convert Django model instance to its ID
        return data.id
    return data
