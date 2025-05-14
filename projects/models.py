from django.db import models
from users.models import Profile
import uuid


class Projects(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']
    
    @property
    def reviwers(self):
        queryset = self.reviews_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        review = self.reviews_set.all()
        upVotes = review.filter(value='up').count()
        totalReviews = review.count()

        if totalReviews > 0:
            ratio = (upVotes / totalReviews) * 100
        else:
            ratio = 0

        self.vote_total = totalReviews
        self.vote_ratio = int(ratio)
        self.save()



class Reviews(models.Model):
    VOTE_TYPE = [
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    ]
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200,choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value
    
    class Meta:
        unique_together = [['owner','project']]
    

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    def __str__(self):
        return self.name
