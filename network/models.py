from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    likes=models.ManyToManyField("Post",blank=True,null=True,related_name="likes")
    profile_image=models.TextField(blank=True,null=True,default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")
    def __str__(self):
        return self.username


class Post(models.Model):
    body=models.CharField(max_length=300)
    date=models.DateTimeField()
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"from {self.user}"


class UserFollowing(models.Model):
    user_id = models.ForeignKey("User", related_name="following",on_delete=models.CASCADE)

    following_user_id = models.ForeignKey("User", related_name="followers",on_delete=models.CASCADE)

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.following_user_id} got new follower"