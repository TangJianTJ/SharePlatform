from rest_framework_mongoengine import serializers
from .models import Student
from .models import Teacher
from django.contrib.auth.hashers import make_password


class StudentSerializers(serializers.DocumentSerializer):
    role = serializers.drf_fields.CharField(read_only=True)

    class Meta:
        model = Student
        fields = ('uid','username','password','name','sex','major','email','creat_time','role','phone')

    def validate(self, attrs):
        password = attrs.get('password')
        if password:
            attrs['password'] = make_password(password)
        # else:
        #     raise serializers.me_ValidationError('密码不能为空')
        return attrs


class TeacherSerializers(serializers.DocumentSerializer):
    role = serializers.drf_fields.CharField(read_only=True)

    class Meta:
        model = Teacher
        fields = ('uid','username','password','name','major','email','phone','creat_time','role','sex')

    def validate(self, attrs):
        password = attrs.get('password')
        if password:
            attrs['password'] = make_password(password)
        # else:
        #     raise serializers.me_ValidationError('密码不能为空')
        return attrs
