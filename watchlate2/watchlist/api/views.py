# from rest_framework.decorators import api_view
from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import (WatchListSerializer,
                          StreamPlatformSerializer, ReviewSerializer)
from watchlist.models import WatchList, PlatformStream, Review
from .permissions import ReviewUserOrReadOnly, IsAdminOrReadOnly
from .throttling import ReviewCreateThrottling
from .pagination import WatchListPagination, WatchListLO, WatchListCursor


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottling]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        user_review = self.request.user
        review = Review.objects.filter(watchlist=watchlist, user_review=user_review)
        if review.exists():
            raise serializer.ValidationError({'error': 'You already made a review'})
        if watchlist.avg_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
        watchlist.number_rating += 1
        watchlist.save()

        serializer.save(watchlist=watchlist, user_review=user_review)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # permission_classes = [IsAuthenticated]

    # override the query set to perform the query that we want
    def get_queryset(self):
        # get the pk in url
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly, ]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


'''
class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()  # the query set we want to make
    serializer_class = ReviewSerializer  # the serializer

    def get(self, request, *args, **kwargs):  # the method we want to make
        return self.list(request, *args, **kwargs)  # list to retrieve many objects

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  # to create an object


class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)  # to retrieve a single object'''


class PlatformStreamAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platforms = PlatformStream.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class PlatformStreamDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = PlatformStream.objects.get(id=pk)
            serializer = StreamPlatformSerializer(platform)
            return Response(serializer.data)
        except PlatformStream.DoesNotExist:
            return Response({'error': 'Not Found'}, status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            platform = PlatformStream.objects.get(id=pk)
            serializer = StreamPlatformSerializer(platform, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except PlatformStream.DoesNotExist:
            return Response({'erros': 'Not Found'}, status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            platform = PlatformStream.objects.get(id=pk)
            platform.delete()
            return Response({'item': 'item has been deleted'}, status.HTTP_204_NO_CONTENT)
        except PlatformStream.DoesNotExist:
            return Response({'item': 'does not exist'}, status.HTTP_404_NOT_FOUND)


class WatchListGV(generics.ListAPIView):
    serializer_class = WatchListSerializer
    queryset = WatchList.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'platform__name']
    # pagination_class = WatchListPagination
    # pagination_class = WatchListLO
    pagination_class = WatchListCursor
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['=title', 'platform__name']
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating', ]


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class WatchListDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(id=pk)
            serializer = WatchListSerializer(movie)
            return Response(serializer.data)
        except WatchList.DoesNotExist:
            return Response({'movie': 'movie is not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(id=pk)
            serializer = WatchListSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WatchList.DoesNotExist:
            return Response({'movie': 'movie was not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(id=pk)
            movie.delete()
            return Response({'movie': 'movie has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        except WatchList.DoesNotExist:
            return Response({'movie': 'movie is not found'}, status=status.HTTP_404_NOT_FOUND)


'''@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = MovieSerializer(WatchList.objects.all(), many=True)
        return Response(movies.data)
    if request.method == 'POST':
        movie = MovieSerializer(data=request.data)
        if movie.is_valid():
            movie.save()
            return Response(movie.data)


@api_view(["GET", "DELETE", "PUT"])
def single_movie(request, pk):
    if request.method == "GET":
        movie = MovieSerializer(WatchList.objects.get(id=pk))
        return Response(movie.data)
    if request.method == "PUT":
        try:
            movie = WatchList.objects.get(id=pk)
        except WatchList.DoesNotExist:
            return Response({'title': 'movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        movie = WatchList.objects.get(id=pk)
        movie.delete()
        return Response({'movie': 'movie has been deleted'}, status=status.HTTP_204_NO_CONTENT)'''
