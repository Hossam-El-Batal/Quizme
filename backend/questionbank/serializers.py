from rest_framework import serializers

from questionbank.models import QuestionBank


class QuestionBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank
        # fields = '__all__'
        exclude = ['user_id']
        read_only_fields = ['id']