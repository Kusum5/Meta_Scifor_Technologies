import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from . import utils


class User(AbstractUser):
    """User project models
    Args: AbstractUser (_type_): Abstract user class
    _type_: Model
    """
    USER_TYPE = (("P", "P"), ("B", "B"))
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = models.SlugField(unique=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)
    otp = models.CharField(max_length=100, null=True, blank=True)
    reset_token = models.CharField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=1, choices=USER_TYPE, default="P")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-date_joined', 'first_name']
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
        email_username, _ = self.email.split('@')

        if not self.last_name:
            self.last_name = ""

        if not self.username:
            self.username = email_username

        if self.is_superuser:
            self.type = 'B'

        if not self.slug:
            self.slug = slugify(f"{self.first_name} {self.last_name} {utils.generate_short_id(4)}")
        return super(User, self).save(*args, **kwargs)


class Sector(models.Model):
    """Enterprise sector models"""
    sid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', 'created_at']
        verbose_name_plural = "Business Sectors"

    def __str__(self) -> str:
        return f"{self.name}"


class AbstractProfile(models.Model):
    """Abstract Profile model"""

    pid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = models.SlugField(unique=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="perfil", blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    address = models.CharField(max_length=255, blank=False)

    website = models.CharField(max_length=255, blank=True, default="")
    linkedin = models.CharField(max_length=255, blank=True, default="")
    facebook = models.CharField(max_length=255, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def image_url(self) -> str:
        """ image url string
        Returns:
            str: image url 
        """
        try:
            url = self.image.url
        except ValueError:
            url = '/static/assets/images/user.png'
        return url


class PersonalProfile(AbstractProfile):
    """Customer profile class model"""
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="personal_profile")
    bi = models.CharField(max_length=14, null=False, unique=True)
    gender = models.CharField(max_length=50, choices=utils.GENDER, default=utils.GENDER[0])
    birthday = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "User Profiles"
        ordering = ["user"]

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        """Get the user full name
        Returns:
            str: user full name string
        """
        return self.user.get_full_name()

    def get_gender(self) -> list:
        """Gets a friendly representation of a gender field."""
        return [item for item in (utils.GENDER)]

    def get_gender_string(self) -> list:
        """Gets a friendly representation of a gender field."""
        return self.gender

    def get_absolute_url(self) -> str:
        """Gets URL for personal detail profile
        Returns:
            str: URL string for the personal profile detail page 
        """
        return reverse("edit-user", kwargs={"slug": self.slug})


class CompanyProfile(AbstractProfile):
    """Company profile class model"""
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="company_profile")
    sector = models.ForeignKey(Sector, models.PROTECT)
    nif = models.CharField(max_length=14, null=False, unique=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Business Profiles"
        ordering = ["user"]

    def get_absolute_url(self) -> str:
        """Gets URL for company detail profile
        Returns:
            str: URL string for the company profile detail page 
        """
        return reverse("edit-user", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.user.get_full_name()
