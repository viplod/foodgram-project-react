from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer)


class UserSerializer(BaseUserSerializer):
    """
    Изменение сериализатора djoser работы с моделью User
    для отображение дополнительных полей.
    """
    class Meta(BaseUserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name')


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Изменение сериализатора djoser работы с моделью User
    при создании нового пользователя для отображение дополнительных полей.
    """
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'password')
