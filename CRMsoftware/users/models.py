# from django.db import models
# from django.contrib.auth import get_user_model
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
#     mobile = models.CharField(max_length=11)
#     graduate = models.CharField(blank=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     joined = models.DateTimeField(auto_now_add=True, db_index=True)
