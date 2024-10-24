""" Business Models """
import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class JobType(models.Model):
    """Job type for representing remote, in-person, hybrid, etc.
    Args:
        models (Model): ORM model
    """
    title = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Job Types'
        ordering = ['title', '-created_at']

    def __str__(self) -> str:
        return f"{self.title}"


class Vacancy(models.Model):
    """Vacancy model"""
    vid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to="perfil", blank=True)
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    city = models.CharField(max_length=255)
    min_wage = models.DecimalField(max_digits=15, decimal_places=2)
    max_wage = models.DecimalField(max_digits=15, decimal_places=2)
    expiration_data = models.DateField()
    entry_time = models.TimeField()
    exit_time = models.TimeField()
    is_published = models.BooleanField(default=True)

    company = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Vacancies'
        ordering = ['-created_at', 'title']

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        """Gets URL for vacancy profile
        Returns:
            str: URL string for vacancy 
        """
        return reverse("business:vacancy-detail", kwargs={"company_slug": self.company.slug,
                                                          "vid": self.vid})

    def image_url(self):
        """Image URL string
        Returns:
            str: Image URL 
        """
        try:
            url = self.image.url
        except ValueError:
            url = self.company.company_profile.image_url
        return url

    def get_skills(self):
        """Get all skills required for this vacancy
        Returns:
            Queryset: Vacancy skills queryset
        """
        return Skill.objects.filter(vacancy=self)

    def get_responsibilities(self):
        """Get all responsibilities required for this vacancy
        Returns:
            Queryset: Vacancy responsibilities queryset
        """
        return Responsibility.objects.filter(vacancy=self)

    def get_benefits(self):
        """Get all benefits required for this vacancy
        Returns:
            Queryset: Vacancy benefits queryset
        """
        return Benefit.objects.filter(vacancy=self)

    def get_job_description(self) -> str:
        job_description = f"Title: {self.title}\n"
        job_description += f"Job Type: {self.job_type}\n"
        job_description += f"Description:\n{self.description}\n"
        job_description += f"Location: {self.city}\n"

        job_description += f"Required Skills:\n"
        for item in self.get_skills():
            job_description += f"{item.title}\n"

        job_description += f"Responsibilities:\n"
        for item in self.get_responsibilities():
            job_description += f"{item.title}\n"

        job_description += f"Benefits:\n"
        for item in self.get_benefits():
            job_description += f"{item.title}\n"
        return job_description


class Benefit(models.Model):
    """Model for employment benefits for the person hiring for the position"""
    bid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Job Benefits'
        ordering = ['title', '-created_at']

    def __str__(self) -> str:
        return f"{self.title}"


class Skill(models.Model):
    """Skill model"""
    sid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Required Skills'
        ordering = ['title', '-created_at']

    def __str__(self) -> str:
        return f"{self.title}"


class Responsibility(models.Model):
    """Model for responsibilities"""
    rid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Responsibilities'
        ordering = ['title', '-created_at']

    def __str__(self) -> str:
        return f"{self.title}"


class Candidate(models.Model):
    """Register vacancy candidates"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    cv = models.FileField(upload_to="candidates/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Applications'
        ordering = ['user', '-created_at']

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.vacancy.title}"

    def get_absolute_url(self):
        """Return the candidate string URL"""
        return reverse("model_detail", kwargs={"pk": self.pk})

    def get_file_details(self):
        """Get details of the uploaded file"""
        file_id = self.id  # Get the file ID (in the database)
        file_name = self.cv.name.split('/')[-1]  # Get the pure file name
        file_path = self.cv.path  # Get the full path of the file
        file_size = self.cv.size  # Get the size of the file in bytes
        file_type = self.cv.name.split('.')[-1]  # Get the file type (extension) 
        return {'name': file_name, 'path': file_path, 'size': file_size, 'id': file_id, 'type': file_type}
