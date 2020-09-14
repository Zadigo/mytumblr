from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, IntegerField, BooleanField

class ProductSerializer(Serializer):
    id      = IntegerField()
    name    = CharField()
    surname = CharField()
    price   = IntegerField()
    checked = BooleanField(default=False)
    selected = BooleanField(default=False)
    deleted = BooleanField(default=False)