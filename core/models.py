from django.db import models


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