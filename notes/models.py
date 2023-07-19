from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce import models as tinymce_models

# Create your models here.

class Note(models.Model):
    """Represents a note """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    note_text = tinymce_models.HTMLField()
    date_created = models.DateTimeField(auto_now=False, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    themes = [
        ('yellow-theme', 'yellow'),
        ('green-theme', 'green'),
        ('pink-theme', 'pink'),
        ('purple-theme', 'purple'),
        ('blue-theme', 'blue'),
        ('gray-theme', 'gray'),
        ('charcoal-theme', 'charcoal') 
    ]

    colour_theme = models.CharField(
        max_length=19,
        choices=themes,
        default='yellow-theme'
    )

    def __str__(self):
        return self.note_text[0:18]
    
    def get_formatted_date_date_created(self):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        today = timezone.now()
        todays_date = today.date()
        date = self.date_created.date()
        month = months[self.date_created.month - 1]
        day = self.date_created.day
        year = self.date_created.year
        hour = str(self.date_created.hour)
        minute = str(self.date_created.minute)

        if (todays_date == date):
            return f"{hour.rjust(2, '0')}:{minute.rjust(2, '0')}"
        elif ((today > self.date_created) and  (today.year > year)):
            return f"{day} {month} {year}"
        if ((today > self.date_created) and (today.year == year)):
            return f"{day} {month}"

    def get_formatted_date_last_updated(self):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        today = timezone.now()
        todays_date = today.date()
        date = self.last_updated.date()
        month = months[self.last_updated.month - 1]
        day = self.last_updated.day
        year = self.last_updated.year
        hour = str(self.last_updated.hour)
        minute = str(self.last_updated.minute)

        if (todays_date == date):
            return f"{hour.rjust(2, '0')}:{minute.rjust(2, '0')}"
        elif ((today > self.date_created) and  (today.year > year)):
            return f"{day} {month} {year}"
        if ((today > self.date_created) and (today.year == year)):
            return f"{day} {month}"

    def has_excess_images(self):
        return len(self.image_set.all()) > 4

    def get_images(self):
        context = {}
        if len(self.image_set.all()) > 4:
            images = list(self.image_set.all())
            context['no_of_extra'] = len(images) - 4
            images.reverse()
            context['added'] = context['no_of_extra'] + 1
            last = images[3]
            context['last_index'] = len(images) - 4
            shown_images = images[:3]
            context['images'] = shown_images
            context['last_image'] = last
            return context
        else:
            images = list(self.image_set.all())
            images.reverse()
            context['images'] = images
            return context

class Image(models.Model):
    """Represents an image attached to a note"""
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    alt_text = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return self.alt_text
    
class DisplayMode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    modes = [
        ('light-mode', 'light'),
        ('dark-mode', 'dark'),
    ]

    display_mode = models.CharField(
        max_length=10,
        choices=modes,
        default='light-mode'
    )

    def __str__(self):
        return self.display_mode