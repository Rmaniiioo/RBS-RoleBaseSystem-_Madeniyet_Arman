from django.db import models

# Create your models here.
class Role(models.Model):
    code = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_system = models.BooleanField(default=False)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.code


class BusinessElement(models.Model):
    code = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.code
        

class AccessRoleRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name= 'access_role')
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE, related_name='role_rules')
    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission =  models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        constraints = [

            models.UniqueConstraint(fields=['role', 'element'], name ='unique_role_element_rule')
        ]
        ordering = ['role__code', 'element__code']

    def __str__(self):
        return f'{self.role.code}:{self.element.code}'
    
    