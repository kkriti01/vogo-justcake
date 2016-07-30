from rest_framework.serializers import ModelSerializer
from cakes.models import Cake


class CakeSerializer(ModelSerializer):

    class Meta:
        model = Cake
