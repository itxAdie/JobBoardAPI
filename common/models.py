from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'user_control.UserModel', related_name='%(class)s_created_by',
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    updated_by = models.ForeignKey(
        'user_control.UserModel', related_name='%(class)s_updated_by',
        on_delete=models.SET_NULL, null=True, blank=True,
    )

    class Meta:  # This is an abstract class and will not be created in the database
        abstract = True


class RequestLog(models.Model):
    user = models.ForeignKey(
        'user_control.UserModel', on_delete=models.CASCADE,
        null=True, blank=True,
    )
    ip_address = models.GenericIPAddressField()
    endpoint = models.CharField(max_length=255)
    status_code = models.IntegerField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_name = self.user.get_full_name() if self.user else 'Anonymous'
        return f"{user_name} - {self.endpoint} - {self.created_at}"
