from django.db import models
from django.conf import settings
from django.db.models.aggregates import Sum


#==========================================================
# Custom Model Managers
#==========================================================
class MovieManager(models.Manager):

    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('writers', 'actors')
        return qs

    def all_with_related_persons_and_score(self):
        qs = self.all_with_related_persons()
        qs = qs.annotate(score=Sum('vote__value'))
        return qs


class PersonManager(models.Manager):

    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'role_set__movie'
        )


class VoteManager(models.Manager):

    def get_vote_or_unsaved_blank_vote(self, movie, user):
        try:
            return Vote.objects.get(
                movie=movie,
                user=user
            )
        except Vote.DoesNotExist:
            return Vote(
                movie=movie,
                user=user
            )


#==========================================================
# Models
#==========================================================
class Movie(models.Model):

    # Choices
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G, 'G - General Audiences'),
        (RATED_PG, 'PG - Parental Guidance'),
        (RATED_R, 'R - Restricted'),
    )

    # Model fields
    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    director = models.ForeignKey(
        to='Person',
        on_delete=models.SET_NULL,
        related_name='directed',
        null=True,
        blank=True
    )
    writers = models.ManyToManyField(
        to='Person',
        related_name='writing_credits',
        blank=True
    )
    actors = models.ManyToManyField(
        to='Person',
        through='Role',
        related_name='acting_credits',
        blank=True
    )

    # Custom Manager class
    objects = MovieManager()

    # Meta class attributes
    class Meta:
        ordering = (
            '-year',
            'title',
        )

    # Human friendly obj representation
    def __str__(self):
        return "{} ({})".format(
            self.title,
            self.year
        )


class Person(models.Model):

    # Model fields
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    # Custom Manager class
    objects = PersonManager()

    # Meta class attributes
    class Meta:
        ordering = (
            'last_name',
            'first_name',
        )

    # Human friendly obj representation
    def __str__(self):
        if self.died:
            return "{}, {} ({}-{})".format(
                self.last_name,
                self.first_name,
                self.born,
                self.died
            )
        else:
            return "{}, {} ({})".format(
                self.last_name,
                self.first_name,
                self.born,
            )


class Role(models.Model):
    movie = models.ForeignKey(to='Movie', on_delete=models.DO_NOTHING)
    person = models.ForeignKey(to='Person', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=140)

    class Meta:
        unique_together = (
            'movie',
            'person',
            'name',
        )

    def __str__(self):
        return "{} {} {}".format(
            self.movie_id,
            self.person_id,
            self.name
        )


class Vote(models.Model):
    # Constants
    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, "👍",),
        (DOWN, "👎",),
    )

    # Model fields
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    # Custom Manager class
    objects = VoteManager()

    # Meta class attributes
    class Meta:
        unique_together = (
            'user', 'movie'
        )