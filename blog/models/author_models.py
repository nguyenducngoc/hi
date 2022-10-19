# Core Django imports.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('profile')
    banner_image = CloudinaryField('banner')
    job_title = models.CharField(max_length=100)
    bio = models.CharField(max_length=100,
                           help_text="Sở thích")

    address = models.CharField(max_length=100,
                               help_text="Nhập địa chỉ của bạn"
                               )

    city = models.CharField(
                            max_length=100, help_text="Thành phố"
                            )

    country = models.CharField(max_length=100,
                               help_text="Quốc gia"
                               )

    zip_code = models.CharField(max_length=100,
                                help_text="Mặc định là: 100000"
                                )

    twitter_url = models.CharField(max_length=250, default="#",
                                   blank=True, null=True,
                                   help_text=
                                   "Tw")
    instagram_url = models.CharField(max_length=250, default="#",
                                     blank=True, null=True,
                                     help_text=
                                     "IG")
    facebook_url = models.CharField(max_length=250, default="#",
                                    blank=True, null=True,
                                    help_text=
                                    "Fb")
    github_url = models.CharField(max_length=250, default="#",
                                  blank=True, null=True,
                                  help_text=
                                  "Gh")

    email_confirmed = models.BooleanField(default=False)

    created_on = models.DateTimeField(default=timezone.now)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
