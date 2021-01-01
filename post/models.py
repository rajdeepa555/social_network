from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Post(models.Model):
    title= models.CharField(max_length=300, unique=True)
    url= models.SlugField(max_length=300)
    content= models.TextField()
    pub_date = models.DateTimeField(auto_now_add= True)
    last_edited= models.DateTimeField(auto_now= True)
    author= models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.url= slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Preference(models.Model):
    ACTIONS_CHOICES =( 
        (1, "like"), 
        (2, "unlike"), 
    ) 
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    action= models.IntegerField(
        choices=ACTIONS_CHOICES,
        null=True,
    )
    date= models.DateTimeField(auto_now= True)

    
    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.action)
