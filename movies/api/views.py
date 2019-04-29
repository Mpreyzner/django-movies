from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MovieSerializer, CommentSerializer
from .models import Movie, Comment
import requests
import os
import json
from django.db.models import Count
import datetime


class MovieAPIListView(APIView):
    """
    get:
    Return a list of all the existing movies

    post:
    Add new movie by title, fetching data from omdbapi
    """
    def get(self, request, format=None):
        # @TODO add some additional filtering and sorting, maybe by year or something
        items = Movie.objects.all()
        serializer = MovieSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if 'title' not in request.data:
            return Response("Movie title missing", status=400)
        title = request.data['title']

        if Movie.objects.filter(title=request.GET['title']).exists():
            serializer = CommentSerializer(Movie.objects.filter(title=request.GET['title']))
            return Response(serializer.data, status=200)

        serializer = MovieSerializer(data=self.get_movie_data(title))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get_movie_data(self, title):
        api_key = os.environ.get('API_KEY')
        api_url = 'http://www.omdbapi.com/'
        response = requests.get(api_url, {'apikey': api_key, 't': title})
        response.raise_for_status()
        # @TODO catch 404 and return response
        data = json.loads(response.content)
        data = {k.lower(): v for k, v in data.items()}
        keys = ('title', 'director', 'writer', 'language', 'country')
        filtered = dict(zip(keys, [data[k] for k in keys]))
        return filtered


class CommentAPIListView(APIView):

    """
    get:
    Return all comments, can be filtered by movie id when movie_id is provided in query

    post:
    Add new comment to a movie
    """
    def get(self, request, format=None):
        # @TODO remove author from comments and create migration
        if 'movie_id' in request.GET:
            items = Comment.objects.filter(movie=request.GET['movie_id'])
        else:
            items = Comment.objects.all()
        serializer = CommentSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if not Movie.objects.filter(movie=request.GET['movie_id']).exists():
            return Response("Movie with id %s does not exist" % request.GET['movie_id'], status=400)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TopAPIListView(APIView):
    """
    get:
    Return movie statistics with movie_id, number of comments and rank (higher rank means more comments)
    """
    def get(self, request, format=None):
        if 'from' in request.GET and 'to' in request.GET:
            date_from = self.get_date(request.GET['from'])
            date_to = self.get_date(request.GET['to'])
        else:
            return Response("Date range for calculating stats required, expected 'from' and 'to'", status=400)

        movies = Movie.objects.select_related() \
            .filter(created__range=[date_from, date_to]) \
            .annotate(comments_count=Count('comment')).order_by('comments_count')

        max_comments = movies.last().comments_count

        stats = []
        for movie in movies:
            if movie.comments_count:
                rank = movie.comments_count - max_comments + 1
            else:
                rank = 0
            stats.append({'rank': rank, 'comments': movie.comments_count, 'id': movie.id})
        return Response(stats)

    def get_date(self, date_text):
        try:
            return datetime.datetime.strptime(date_text, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Incorrect data format, should be DD-MM-YYYY")
