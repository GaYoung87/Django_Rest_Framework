from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-pk', )  # 마지막으로 작성된 것이 첫번째로 보일 수 있도록 하는 것
        # ordering은 tuple이나 list 가능 -> 

    def __str__(self):
        return f'{self.pk} - {self.title}'
