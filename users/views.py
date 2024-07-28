# users/views.py
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
# users/views.py
from confluent_kafka import Producer
from django.conf import settings

# Kafka producer configuration
producer = Producer({'bootstrap.servers': settings.KAFKA_BROKER_URL})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        producer.produce(settings.KAFKA_TOPIC, key=str(user.id), value=user.email)
        producer.flush()
