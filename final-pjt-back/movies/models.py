from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User

# Create your models here.
# class Genre(models.Model):
#     genre = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    nation = models.CharField(max_length=10)
    running_time = models.IntegerField()
    release_date = models.DateField()
    overview = models.TextField()
    genre_ids = models.IntegerField()
    genres = models.JSONField(default=list)
    poster_path = models.TextField()
    backdrop_path = models.TextField(null=True)
    popularity = models.FloatField()
    actual_vote_average = models.FloatField()
    man_vote = models.FloatField()
    woman_vote = models.FloatField()
    vote_10 = models.FloatField()
    vote_20 = models.FloatField()
    vote_30 = models.FloatField()
    vote_40 = models.FloatField()
    vote_50 = models.FloatField()
    # 관람가 정보
    grade = models.IntegerField()
    # 배우정보 (네이버에서 긁어옴)
    actors = models.CharField(max_length=100)
    video_url = models.TextField()
    profile = models.JSONField(default=list)

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def nickname(self,):
        user_nickname = User.objects.get(pk=self.user.pk).nickname
        return user_nickname

       