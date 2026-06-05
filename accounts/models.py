from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    role = models.ForeignKey('access_control.Role', on_delete=models.PROTECT, related_name='users')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    delete_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return ' '.join(part for part in parts if part)
    
    @property
    def is_authenticate(self):
        return self.is_active
    
    def soft_delete(self):
        self.is_active = False
        self.delete_at = timezone.now()
        self.save(update_fieilds=['is_active', 'delete_at','update_at'])


class RevokedToken(models.Model):
    jti = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    revoked_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


    class Meta:
        ordering = ['-revoked_at']

    def __str__(self):
        return self.jti