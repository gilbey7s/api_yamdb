from django.db import models
from django.contrib.auth import get_user_model #Думаю тут нужно создать кастомную модель в отдельном приложении

User = get_user_model()

from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    text = models.TextField(null=False, verbose_name="Отзыв")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True
    )
    score = models.IntegerField(
        'Оценка', validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Оцените от 1 до 10",)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews') #Тайтл надо будет дописать

    class Meta:
        ordering = ['id']
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review')
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
