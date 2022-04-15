from rest_framework import serializers
from watchlist.models import WatchList, PlatformStream, Review


class ReviewSerializer(serializers.ModelSerializer):
    user_review = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ['watchlist', ]


class WatchListSerializer(serializers.ModelSerializer):
    # Nested Serializer
    # reviews = ReviewSerializer(many=True, read_only=True)
    # to create a specific field that does not exist in our Model
    name_length = serializers.SerializerMethodField()
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = WatchList
        fields = '__all__'

        # fields = ['id', 'storyline', 'title']
        # exclude = ['active', ]

    def get_name_length(self, object):
        # object has the access to all the model attribute
        return len(object.title)

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("title is too short!")
        return value

    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError("title and storyline should not be the same")
        return data


class StreamPlatformSerializer(serializers.ModelSerializer):
    # Nested serializer many to one
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = PlatformStream
        fields = "__all__"


'''
def name_length(value):
    if value == 'MongoDb':
        raise serializers.ValidationError('title should be different from MongoDb')


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(validators=[name_length, ])
    storyline = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validate_data):
        return WatchList.objects.create(**validate_data)

    def update(self, instance, validate_data):
        instance.title = validate_data.get('title', instance.title)
        instance.storyline = validate_data.get('storyline', instance.storyline)
        instance.active = validate_data.get('active', instance.active)
        instance.save()
        return instance

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("title is too short!")
        return value

    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError("title and storyline should not be the same")
        return data'''
