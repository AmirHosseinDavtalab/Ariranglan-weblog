from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django.template.defaultfilters import slugify
from django_resized import ResizedImageField


# Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'dr', 'انتظار'
        PUBLISHED = 'pu', 'منتشر کردن'
        REJECTED = 're', 'رد کردن'

    CATEGORY_CHOICES = (
        ('انیمه', 'انیمه'),
        ('سریال', 'سریال'),
        ('گردشگری', 'گردشگری'),
        ('برنامه نویسی', 'برنامه نویسی'),
        ('آشپزی', 'آشپزی'),
        ('مدلینگ', 'مدلینگ'),
        ('طراحی', 'طراحی'),
        ('متفرقه', 'متفرقه'),
    )
    # relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name="نویسنده")
    # data fields
    title = models.CharField(max_length=250, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    slug = models.SlugField(max_length=250, verbose_name="اسلاگ")
    # Date
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name="انتشار")
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    status = models.CharField(max_length=2, default=Status.DRAFT, choices=Status.choices, verbose_name="وضعیت")
    reading_time = models.PositiveIntegerField(default=0, verbose_name='زمان مطالعه')

    # managers
    objects = jmodels.jManager()
    published = PublishedManager()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='متفرقه')

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


class Ticket(models.Model):
    name = models.CharField(max_length=250, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    subject = models.CharField(max_length=250, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="پست")
    name = models.CharField(max_length=250, verbose_name='نام')
    text = models.TextField(verbose_name='متن کامنت')
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ آپدیت')
    active = models.BooleanField(default=False, verbose_name='وضعیت')

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f'{self.name} : {self.post}'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name="تصویر")
    image_file = ResizedImageField(upload_to='post_images/', size=[200, 300], crop=['middle', 'center'])
    title = models.CharField(max_length=250, verbose_name="عنوان", null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"

    def __str__(self):
        return self.title or 'No Title'

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ تولد')
    bio = models.TextField(verbose_name="بایو", null=True, blank=True)
    photo = ResizedImageField(verbose_name='تصویر پروفایل', blank=True, null=True, upload_to='profile_images/',
                              size=[200, 200], quality=70, crop=['middle', 'center'])
    job = models.CharField(verbose_name="شغل", null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل ها"
