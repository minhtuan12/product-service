from djongo import models

from book_categories.models import Category

# Create your models here.

BOOK_STATUS = {
    'UNAVAILABLE': 0,
    'AVAILABLE': 1
}


class Book(models.Model):
    _id = models.ObjectIdField()
    code = models.CharField(max_length = 50)
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    description = models.TextField(null = True, blank = True)
    price = models.PositiveBigIntegerField()
    old_price = models.PositiveBigIntegerField(default = None, null = True, blank = True)
    image = models.ImageField(upload_to = 'images/', null = True, blank = True, default = None)
    status = models.PositiveIntegerField(default = BOOK_STATUS['AVAILABLE'])
    quantity = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted = models.PositiveBigIntegerField(default = 0)
    categories = models.ManyToManyField(Category)

    class Meta:
        db_table = 'books'
        verbose_name_plural = 'Books'

    ordering = ['-created_at']

    def __str__(self):
        return self.code
