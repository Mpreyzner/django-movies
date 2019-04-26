from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MovieSerializer, CommentSerializer
from .models import Movie, Comment


class MovieAPIListView(APIView):

    def get(self, request, format=None):
        # 2. Additional filtering, sorting is fully optional - but some implementation is a bonus (pagination, filter by year etc)
        items = Movie.objects.all()
        serializer = MovieSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # 1. ​Request body should contain only movie title, and its presence should be validated.
        # 2. Based on passed title, other movie details should be fetched from http://www.omdbapi.com/ (or other similar, public movie database) - and saved to application database.
        # 3. Request response should include full movie object, along with all data fetched from external API.
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CommentAPIListView(APIView):

    def get(self, request, format=None):
        if 'movie_id' in request.GET:
            items = Comment.objects.filter(movie=request.GET['movie_id'])
        else:
            items = Comment.objects.all()
        serializer = CommentSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # 1. ​Request body should contain ID of movie already present in database, and comment text body.
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TopAPIListView(APIView):

    def get(self, request, format=None):
        # 1.  ​Should return top movies already present in the database ranking based on a number of comments added to the movie (as in the example) in the *specified date range*.
        # The response should include the ID of the movie, position in rank and total number of comments (in the specified date range).
        # 2. Movies with the same number of comments should have the same position in the ranking.
        # 3. Should require specifying a date range for which statistics should be generated.

        # add date range from and to ->? required
        # find comments from given date range
        # calculate which movies has most comments
        # return statistics

        items = Comment.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
