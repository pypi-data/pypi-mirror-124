import ast
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password, ValidationError

from db.models import (
    User,
    UserProfile,
    Symbol,
    Universe,
    Strategy,
    Log,
    CryptoMinuteData,
    CryptoHourData,
    Signal,
    PairSignal,
    Order,
    Fill,
    OrderSuccess,
)


# [User + UserProfile]
class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_profile(self, obj):
        """
        profile이 생성되지 않았다면 profile 모델을 생성해주고 다음 스텝으로 넘어간다.
        """
        if not hasattr(obj, 'profile'):
            profile = UserProfile(user=obj)
            profile.save()
        skip_keys = ['_state', 'id', 'user_id']
        profile = obj.profile.__dict__
        profile = {key: val for key, val in profile.items() if key not in skip_keys}
        return profile

    def create(self, validated_data):
        if 'profile' in validated_data.keys():
            profile_data = validated_data.pop('profile')
        else:
            profile_data = {}

        password = validated_data.pop('password')
        try:
            validate_password(password)
        except ValidationError as e:
            msgs = ast.literal_eval(str(e))
            raise serializers.ValidationError({'detail': msgs})

        del validated_data['groups']
        del validated_data['user_permissions']
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        """
        updating password
        """
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        password = validated_data.pop('password')
        instance.set_password(password)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


# [Symbol]
class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = '__all__'


# [Universe]
class UniverseSymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ['id', 'symbol_id']


class UniverseSerializer(serializers.ModelSerializer):
    symbols = UniverseSymbolSerializer(many=True, read_only=True)

    class Meta:
        model = Universe
        fields = '__all__'


# [Strategy]
class StrategyUniverseSerializer(serializers.ModelSerializer):
    symbols = serializers.StringRelatedField(many=True)

    class Meta:
        model = Universe
        fields = ['name', 'symbols']


class StrategySerializer(serializers.ModelSerializer):
    universe = StrategyUniverseSerializer(read_only=True)

    class Meta:
        model = Strategy
        fields = '__all__'


# [Log]


# [CryptoMinuteData]


# [CryptoHourData]
class CryptoHourDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoHourData
        fields = '__all__'


# [Signal]
class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = '__all__'


# [PairSignal]
class PairSignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PairSignal
        fields = '__all__'


# [Order]
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


# [Fill]
class FillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fill
        fields = '__all__'


# [OrderSuccess]
class OrderSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSuccess
        fields = '__all__'
