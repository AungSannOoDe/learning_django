# from rest_framework import serializers
# from to_do_app.models import Movie
# class MovieSeralizer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField()
#     description=serializers.CharField()
#     review=serializers.FloatField()
#     active=serializers.BooleanField()

#     def create(self,validate_data):
#         return Movie.objects.create(**validate_data)
#     def update(self,instance,validated_data):
#         instance.name=validated_data.get("name",instance.name)
#         instance.description=validated_data.get("description",instance.description)
#         instance.review=validated_data.get("review",instance.review)
#         instance.active=validated_data.get("active",instance.active)
#         instance.save()
#         return instance
from rest_framework import serializers
from to_do_app.models import Movie, StreamPlatform, WatchList,Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        exclude = ('watchlist',)

class MovieSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def get_len_name(self, object):
        return len(object.name)


class WatchListSerializer(serializers.ModelSerializer):
    review=ReviewSerializer(many=True,read_only=True)
    len_title = serializers.SerializerMethodField()
    
    class Meta:
        model = WatchList  # Fixed: changed 'watchlist' to 'model'
        exclude=('platform',)

    def get_len_title(self, object):
        return len(object.title)


class StreamPlatformSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()
    watchlist=WatchListSerializer(many=True,read_only=True)
    # watchlist=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name="watch_detail")
    class Meta:
        model = StreamPlatform  # Fixed: changed 'stream' to 'model'
        fields = "__all__"

    def get_len_name(self, object):
        return len(object.name)