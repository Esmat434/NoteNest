from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators = [UniqueValidator(queryset=User.objects.all())],
        error_messages = {
            "Invalid":"This email exists enter a valid email adddress"
        }
    )
    username = serializers.CharField(
        required=True,
        validators = [UniqueValidator(queryset=User.objects.all())],
        error_messages = {
            "Invalid":"This username exists enter a valid username."
        }
    )
    phone_number = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())],
        error_messages = {
            "Invalid":"This phone_number exists enter a valid phone_number."
        }
    )
    password = serializers.CharField(write_only=True,validators = [validate_password],required=True)
    password2 = serializers.CharField(write_only=True,required = True)

    class Meta:
        model = User
        fields = (
            'username','email','phone_number','password','password2','first_name','last_name','country',
            'city','birth_date','last_login_ip','last_login'
        )
        extra_kwargs = {
            "first_name":{'required':False},
            "last_name":{'required':False},
            "country":{'required':False},
            "city":{'required':False},
            "birth_date":{'required':True},
            "last_login_ip":{'required':False},
            "last_login":{'required':False}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password do not match."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
            password = validated_data['password'],
            first_name = validated_data.get('first_name',''),
            last_name = validated_data.get('last_name',''),
            picture = validated_data.get('picture',''),
            address = validated_data.get('address',''),
            country = validated_data.get('country',''),
            city = validated_data.get('city',''),
            birth_date = validated_data.get('birth_date',''),
            last_login_ip = validated_data.get('last_login_ip','')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username','email','first_name','last_name','phone_number','picture','country',
            'city','birth_date','password'
            )
        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user','is_enable','created_time','updated_time']