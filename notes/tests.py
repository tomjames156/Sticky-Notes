from django.test import TestCase
from django.urls import reverse
from notes.models import Note, Image, DisplayMode
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from notes_app import settings
from django.core.files.uploadedfile import SimpleUploadedFile

def create_default_user():
    user = User.objects.create_user(username='te_amo', email="tomakinenoch@gmail.com", password="him")
    DisplayMode.objects.create(user=user, display_mode="light-mode")
    return user

def create_new_active_user():
    new_active_user = User.objects.create_user(username='tomer', email='tomisinak156@gmail.com', password='greenIgzNHem')
    DisplayMode.objects.create(user=new_active_user, display_mode="dark-mode")
    return new_active_user

def create_new_inactive_user():
    new_inactive_user = User.objects.create_user(username='timmytim', email='stickynotesapp605@gmail.com', password='rosettastown')
    DisplayMode.objects.create(user=new_inactive_user, display_mode="light-mode")
    new_inactive_user.is_active = False
    new_inactive_user.save()
    return new_inactive_user

def create_new_note(note_text, user, days_offset):
    date = timezone.now() + timedelta(days=days_offset)
    new_note = Note.objects.create(note_text=note_text, user=user, date_created=date)
    return new_note



class NoteModelTest(TestCase):
    def setUp(self):
        default_user = create_default_user()
        tomer = create_new_active_user()
        create_new_inactive_user()
        create_new_note('Hey there', default_user, -1)
        create_new_note('Hey there from the future', tomer, 300)

    # tests for a note with a past date
    def test_note_successfully_created(self):
        past_note = Note.objects.get(pk=1)
        future_note = Note.objects.get(pk=2)
        self.assertEqual(past_note.note_text, "Hey there")
        self.assertEqual(future_note.note_text, "Hey there from the future")

    def test_note_correct_date(self):
        past_note = Note.objects.get(pk=1)
        future_note = Note.objects.get(pk=2)
        self.assertTrue(past_note.date_created <= timezone.now())
        self.assertTrue(future_note.date_created >= timezone.now())

    def test_note_default_colour(self):
        past_note = Note.objects.get(pk=1)
        future_note = Note.objects.get(pk=2)
        future_note.colour_theme = 'green-theme'
        future_note.save()
        self.assertEqual(past_note.colour_theme, 'yellow-theme')
        self.assertNotEqual(future_note.colour_theme, 'yellow-theme')

    def test_note_view(self):
        response_1 = self.client.post('/notes/1', follow=True) # logged in as the default user
        response_2 = self.client.post('/notes/2', follow=True) 
        self.assertTrue(list(response_1.context['messages']) == [])
        self.assertEqual(str(list(response_2.context['messages'])[0]), "The note you tried to access does not exist on your account") # not logged in as tomer

    def test_show_current_notes_only(self):
        response_1 = self.client.post('/notes/1', follow=True) # default user/ not logged in
        self.client.login(username='tomer', password="greenIgzNHem") # logged in as tomer]
        response_2 = self.client.post('/notes/2', follow=True)
        self.assertTrue(list(response_1.context['messages']) == [])
        self.assertEqual(str(list(response_2.context['messages'])[0]), "The note you tried to view does not exist yet")

    def test_note_has_no_images(self):
        past_note = Note.objects.get(pk=1)
        future_note = Note.objects.get(pk=2)
        self.assertTrue(list(past_note.image_set.all()) == [])
        self.assertTrue(list(future_note.image_set.all()) == [])

    def test_create_new_note_view_default_user(self):
        # default user
        url = reverse('notes:new_note', args=['purple-theme'])
        response = self.client.post(url[:-1], follow=True)
        note = response.context['note']
        self.assertEqual(note.user.username, 'te_amo')
        self.assertEqual(note.colour_theme, 'purple-theme')
        self.assertEqual(response.context['theme'], 'light-mode')

    def test_create_new_note_view_logged_in(self):
        # log in as tomer
        self.client.login(username='tomer', password="greenIgzNHem")
        url = reverse('notes:new_note', args=['blue-theme'])
        response = self.client.post(url[:-1], follow=True)
        note = response.context['note']
        self.assertEqual(note.user.username, 'tomer')
        self.assertEqual(note.colour_theme, 'blue-theme')
        self.assertEqual(response.context['theme'], 'dark-mode')

    def test_change_note_color_view(self):
        note_default_user = Note.objects.get(pk=1)
        self.assertEqual(note_default_user.colour_theme, 'yellow-theme')
        note_logged_in_user = Note.objects.get(pk=2)
        self.assertEqual(note_logged_in_user.colour_theme, 'yellow-theme')
        url_1 = reverse('notes:colour', args=[1, 'pink'])
        url_2 = reverse('notes:colour', args=[2, 'gray'])
        self.client.post(url_1[:-1], follow=True) # default user
        self.client.login(username="tomer", password="greenIgzNHem") # logged in as tomer
        response_2 = self.client.post(url_2[:-1], follow=True)
        self.assertTrue(Note.objects.get(pk=1).colour_theme == 'pink-theme')
        self.assertEqual(str(list((response_2.context['messages']))[0]),"The note you tried to modify does not exist yet")

    def test_update_note(self):
        url_1 = reverse('notes:update', args=[1])
        url_2 = reverse('notes:update', args=[2])
        new_text = {'note': 'Hey there👋🏾, my good friend'}
        self.client.post(url_1, new_text, follow=True)
        self.client.post(url_2, new_text, follow=True)
        self.assertEqual(Note.objects.get(pk=1).note_text, new_text['note'])
        # not supposed to be able to update this but its not an api so no p
        self.assertEqual(Note.objects.get(pk=2).note_text, new_text['note'])
        

    def test_delete_note(self):
        url_1 = reverse('notes:delete', args=[1])
        url_2 = reverse('notes:delete', args=[2])
        response_1 = self.client.post(url_1[:-1], follow=True)
        response_2 = self.client.post(url_2[:-1], follow=True)
        self.assertEqual(str(list(response_1.context['messages'])[0]), "Note successfully deleted")
        self.assertEqual(str(list(response_2.context['messages'])[0]), "You cannot delete that note from this account")\





class HomeViewTest(TestCase):
    def setUp(self):
        default_user = create_default_user()
        tomer = create_new_active_user()
        create_new_inactive_user()
        create_new_note('Hey there', default_user, -1)
        create_new_note('Hello from the other side 😮', default_user, -1)
        create_new_note('Hey there👋🏾, my good friend', default_user, 2)
        create_new_note('Hey there from the future', tomer, 300)
        create_new_note('How do you do?, my frieeeend🎶', default_user, -1)

    def test_home_view(self):
        response_1 = self.client.post('/', follow=True)
        default_user = User.objects.get(username="te_amo")
        active_user = User.objects.get(username="tomer")
        default_notes = Note.objects.filter(user=default_user, note_text__gt=0, date_created__lte=timezone.now()).order_by('-last_updated')
        self.assertEqual(list(response_1.context['notes']), list(default_notes))
        self.assertTrue(len(list(response_1.context['notes'])) == 2)
        self.client.login(username="tomer", password="greenIgzNHem") # logged in as tomer
        other_notes = Note.objects.filter(user=active_user, note_text__gt=0, date_created__lte=timezone.now()).order_by('-last_updated')
        response_2 = self.client.post('/', follow=True)
        self.assertEqual(list(response_2.context['notes']), list(other_notes))



class NoteViewTest(TestCase):
    def setUp(self):
        default_user = create_default_user()
        tomer = create_new_active_user()
        create_new_inactive_user()
        create_new_note('Hey there', default_user, -1)
        create_new_note('Hello from the other side 😮', default_user, -1)
        create_new_note('Hey there👋🏾, my good friend', default_user, 2)
        create_new_note('Hey there from the future', tomer, 300)
        create_new_note('How do you do?, my frieeeend🎶', default_user, -1)

    def test_open_note(self):
        url_1 = reverse('notes:note', args=[1])
        url_2 = reverse('notes:note', args=[4])
        response_1 = self.client.post(url_1[:-1], follow=True)
        response_2 = self.client.post(url_2[:-1], follow=True)
        self.assertEqual(response_1.context['note'], Note.objects.get(pk=1))
        self.assertEqual(str(list(response_2.context['messages'])[0]), "The note you tried to access does not exist on your account")

    def test_add_image_to_note(self):
        image_path = settings.test_image_path
        
        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()

        saved_image = SimpleUploadedFile('cute_monkey.jpeg', image_content, content_type='image/jpeg')
        url = reverse('notes:add_image', args=[1])
        self.client.post(url, {'new_image': saved_image}, follow=True)
        self.assertTrue(len(Note.objects.get(pk=1).image_set.all()) == 1)
        cute_monkey_image = Image.objects.get(pk=1)
        url_1 = reverse('notes:view_image', args=[1, 0])
        response_1 = self.client.post(url_1[:-1], follow=True)
        self.assertEqual(list(response_1.context['images']), [cute_monkey_image])
        self.assertEqual(list(response_1.context['images'])[0].alt_text, '')
        self.assertEqual(response_1.context['note'], Note.objects.get(pk=1))
        # test describe image
        url_2 = reverse('notes:describe', args=[1, 0, 1])
        self.client.post(url_2, {"alt_text": 'cutest monkey ever'}, follow=True)
        self.assertEqual(Image.objects.get(pk=1).alt_text, 'cutest monkey ever')
        url_2 = reverse('notes:delete_img', args=[1, 0, 1])
        self.client.post(url_2, follow=True)
        self.assertEqual(list(Image.objects.all()), [])
    

    def test_delete_from_gallery(self):
        image_path = settings.test_image_path
        
        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()

        saved_image = SimpleUploadedFile('cute_monkey.jpeg', image_content, content_type='image/jpeg')
        url = reverse('notes:add_image', args=[1])
        self.client.post(url, {'new_image': saved_image}, follow=True)
        delete_url = reverse('notes:delete_img_from_gal', args=[1, 0, 1])
        self.client.post(delete_url, follow=True)
        self.assertEqual(list(Image.objects.all()), [])



# test whether how the code has been working with a new email to check how the display modes were 

# add that f function to handle race conditions