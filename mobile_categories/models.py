from djongo import models


# Create your models here.

class Category(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length = 50)
    description = models.TextField(default = '', null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted = models.PositiveBigIntegerField(default = 0)

    class Meta:
        db_table = 'mobile_categories'
        verbose_name_plural = 'Categories'

    ordering = ['-created_at']

    def __str__(self):
        return self.name
