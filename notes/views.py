from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from notes.models import Note, Image, DisplayMode
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import ImageUploadForm
from .search_module import search_note, create_regex_pattern
import sys

def page_not_found_view(request, exception):
    return render(request, "errors/404.html")

def server_error(request):
    return render(request, 'errors/500.html', status=500)

def make_new_note(request):    
    default_user = User.objects.get(username="te_amo")
    if request.user.is_authenticated:
        try:
            Note.objects.get_or_create(user=request.user, note_text__lt=1)
        except Note.MultipleObjectsReturned:
            print()
    else:
        try:
            Note.objects.get_or_create(user=default_user, note_text__lt=1)
        except Note.MultipleObjectsReturned:
            print()


def home(request):
    default_user = User.objects.get(username="te_amo")
    if request.user.is_authenticated:
        make_new_note(request)
        if list(DisplayMode.objects.filter(user=request.user)) == []:
            DisplayMode.objects.create(display_mode='dark-mode', user=request.user)
        notes = Note.objects.filter(note_text__gt=0, user=request.user, date_created__lte=timezone.now()).order_by('-last_updated')
        if list(notes) == []:
            messages.warning(request, ('There are currently no notes available. Click the <strong>"+"</strong> button to add some'))
            error_message_no_search_results = '🚫 No notes available'
        else:
            error_message_no_search_results = 'No search results found😗'
        context = {
        "notes": notes,
        "theme": DisplayMode.objects.filter(user=request.user)[0].display_mode,
        'empty_note': list(Note.objects.filter(note_text='', user=request.user))[-1],
        'error_message_enter_text': 'Please enter some text',
        'error_message_no_search_results': error_message_no_search_results
        }
    else:
        make_new_note(request)
        notes = Note.objects.filter(note_text__gt=0, user=default_user, date_created__lte=timezone.now()).order_by('-last_updated')
        if list(notes) == []:
            messages.warning(request, ('There are currently no notes available. Click the <strong>"+"</strong> button to add some'))
            error_message_no_search_results = '🚫 No notes available'
        else:
            error_message_no_search_results = 'No search results found😗'

        context = {
            "notes": notes,
            "theme": DisplayMode.objects.filter(user=default_user)[0].display_mode,
            'empty_note': list(Note.objects.filter(note_text='', user=default_user))[-1],
            'error_message_enter_text': 'Please enter some text',
            'error_message_no_search_results': error_message_no_search_results
        }

    return render(request, 'notes/home.html', context)

def change_display_mode(request, display_mode_index):
    default_user = User.objects.get(username="te_amo")
    modes = ['light-mode', 'dark-mode']
    if request.user.is_authenticated:
        current_theme = DisplayMode.objects.filter(user=request.user)[0]
        current_theme.display_mode = modes[display_mode_index]
        current_theme.save()
    else:
        current_theme = DisplayMode.objects.filter(user=default_user)[0]
        current_theme.display_mode = modes[display_mode_index]
        current_theme.save()
    return HttpResponseRedirect(reverse('notes:home'))

def search_notes(request):
    default_user = User.objects.get(username="te_amo")
    make_new_note(request)
    if request.user.is_authenticated:
        notes = Note.objects.filter(note_text__gt=1, user=request.user, date_created__lte=timezone.now()).order_by('-last_updated')
        if list(notes) == []:
            error_message_no_search_results = '🚫 No notes available'
        else:
            error_message_no_search_results = 'No search results found😗'
        empty_note = list(Note.objects.filter(note_text='', user=request.user))[-1]
    else:
        notes = Note.objects.filter(note_text__gt=1, user=default_user, date_created__lte=timezone.now()).order_by('-last_updated')
        if list(notes) == []:
            error_message_no_search_results = '🚫 No notes available'
        else:
            error_message_no_search_results = 'No search results found😗'
        empty_note = list(Note.objects.filter(note_text='', user=default_user))[-1],
    
    context = {
        'notes': notes,
        'error_message_enter_text': 'Please enter some text',
        'error_message_no_search_results': error_message_no_search_results,
        'empty_note': empty_note,
        }
    
    if request.method == 'POST':
        query_val = request.POST['q']
        if(query_val != ''):
            if request.user.is_authenticated:
                notes = Note.objects.filter(user=request.user).filter(note_text__iregex=rf"{create_regex_pattern(query_val)}", date_created__lte=timezone.now()).order_by('-last_updated')
            else:
                notes = Note.objects.filter(user=default_user).filter(note_text__iregex=rf"{create_regex_pattern(query_val)}", date_created__lte=timezone.now()).order_by('-last_updated')
            for note in notes:
                note.note_text = search_note(query_val, note.note_text)
            context['notes'] = notes
    else:
        messages.error(request, ('No input was submitted to the form'))
        return redirect('notes:home')

    return render(request, 'partials/results.html', context)


def note_view(request, pk):
    default_user = User.objects.get(username="te_amo")
    if request.user.is_authenticated:
        theme = DisplayMode.objects.filter(user=request.user)[0].display_mode
        try:
            note = Note.objects.get(user=request.user, pk=pk)
            if timezone.now() < note.date_created:
                messages.error(request, ("The note you tried to view does not exist yet"))
                return redirect('notes:home')
        except (KeyError, Note.DoesNotExist):
            messages.error(request, ("The note you tried to access does not exist on your account"))
            return redirect('notes:home')
    else:
        theme = DisplayMode.objects.filter(user=default_user)[0].display_mode
        try:
            note = Note.objects.get(user=default_user, pk=pk)
            if timezone.now() < note.date_created:
                messages.error(request, ("The note you tried to view does not exist yet"))
                return redirect('notes:home')
        except (KeyError, Note.DoesNotExist):
            messages.error(request, ("The note you tried to access does not exist on your account"))
            return redirect('notes:home')
    context = {
        'note' : note,
        'theme': theme,
        'form': ImageUploadForm()
    }
    return render(request, 'notes/note.html', context)

def new_note(request, colour_theme):
    default_user = User.objects.get(username="te_amo")
    if request.user.is_authenticated:
        make_new_note(request)
        empty_notes = Note.objects.filter(note_text__lt=1, user=request.user)
        theme = DisplayMode.objects.filter(user=request.user)[0].display_mode
    else:
        make_new_note(request)
        empty_notes = Note.objects.filter(note_text__lt=1, user=default_user)
        theme = DisplayMode.objects.filter(user=default_user)[0].display_mode

    empty_notes.update(colour_theme=colour_theme, date_created=timezone.now())

    return render(request, 'notes/note.html', context={
        'note': empty_notes[0],
        'theme': theme
    })


def change_colour(request, pk, colour):
    default_user = User.objects.get(username="te_amo")
    note = Note.objects.filter(pk=pk)
    if list(note) != []:
        if request.user.is_authenticated:
            try:
                note = Note.objects.get(user=request.user, pk=pk)
                if note.date_created > timezone.now():
                    messages.error(request, ("The note you tried to modify does not exist yet"))
                    return redirect('notes:home')
                note.colour_theme = f"{colour}-theme"
                note.save()
            except (KeyError, Note.DoesNotExist):
                messages.error(request, ("The note you tried to modify does not exist on your account"))
                return redirect('notes:home')
        else:
            try:
                note = Note.objects.get(user=default_user, pk=pk)
                if note.date_created > timezone.now():
                    messages.error(request, ("The note you tried to modify does not exist yet"))
                    return redirect('notes:home')
                note.colour_theme = f"{colour}-theme"
                note.save()
            except (KeyError, Note.DoesNotExist):
                messages.error(request, ("The note you tried to modify does not exist on this account"))
                return redirect('notes:home')
    else:
        messages.error(request, ("The note you tried to modify does not exist"))
        return redirect('notes:home')
    return HttpResponseRedirect(reverse('notes:note', args=[pk]))


def delete_note(request, pk):
    default_user = User.objects.get(username="te_amo")
    note = Note.objects.filter(pk=pk)
    if list(note) != []:
        if request.user.is_authenticated:
            try:
                note = Note.objects.get(user=request.user, pk=pk)
                if note.date_created > timezone.now():
                    messages.error(request, ("The note you tried to delete does not exist yet"))
                    return redirect('notes:home')
                note.delete()
                messages.success(request, ("Note successfully deleted"))
            except (KeyError, Note.DoesNotExist):
                messages.error(request, ("You cannot delete that note from this account"))
                return redirect('notes:home')
        else:
            try:
                note = Note.objects.get(user=default_user, pk=pk)
                if note.date_created > timezone.now():
                    messages.error(request, ("The note you tried to delete does not exist yet"))
                    return redirect('notes:home')
                note.delete()
                messages.success(request, ("Note successfully deleted"))
            except (KeyError, Note.DoesNotExist):
                messages.error(request, ("You cannot delete that note from this account"))
                return redirect('notes:home')
    else:
        messages.error(request, ("The note you tried to delete does not exist"))
    return HttpResponseRedirect(reverse('notes:home'))


def update(request, pk):
    if request.method == 'POST':
        new_text = request.POST['note']
        Note.objects.filter(pk=pk).update(note_text=new_text, last_updated=timezone.now())
        return HttpResponse("Everything stays")
    else:
        messages.error(request, ('No input was submitted to the form'))
        return redirect('notes:home')
    
def add_image(request, pk):
    if request.method == 'POST':
        file = request.FILES['new_image']   
        note = Note.objects.get(pk=pk)
        Image.objects.create(note=note, image=file)
        Note.objects.filter(pk=pk).update(last_updated=timezone.now())
    else:
        messages.error(request, ('No input was submitted to the form'))
        return redirect('notes:home')

    return HttpResponseRedirect(reverse('notes:note', args=[pk]))

def view_image(request, pk, image_index):
    default_user = User.objects.get(username="te_amo")
    if request.user.is_authenticated:
        note = Note.objects.filter(user=request.user, pk=pk)
        if list(note) != []:
            note = Note.objects.get(user=request.user, pk=pk)
            images = note.image_set.all()
            if len(images) > 0:
                context = {}
                context['note'] = note
                context['images'] = images
                context['current_index'] = image_index
                try:
                    context['current_image'] = images[image_index]
                    if image_index + 1 < len(images):
                        context['previous_image'] = images[image_index + 1]
                        context['previous_image_index'] = image_index + 1
                    if image_index - 1 >= 0:
                        context['next_image'] = images[image_index - 1]
                        context['next_image_index'] = image_index - 1
                except IndexError:
                    messages.error(request, ("The image you tried to access does not exist"))
                    return HttpResponseRedirect(reverse('notes:note', args=[pk]))

                context['display_mode'] = DisplayMode.objects.filter(user=request.user)[0].display_mode

                return render(request, 'notes/image_gallery.html', context)
            else:
                messages.error(request, ("The note you tried to access does not have any images"))
                return HttpResponseRedirect(reverse('notes:note', args=[pk]))
        else:
            try:
                note = Note.objects.get(pk=pk)
                messages.error(request, ("You do not have access to this note"))
            except (KeyError, Note.DoesNotExist):
                messages.error(request, ("The note you tried to access does not exist"))
            return redirect('notes:home')
    else:
        note = Note.objects.filter(user=default_user, pk=pk)
        if list(note) != []:
            note = Note.objects.get(user=default_user, pk=pk)
            images = note.image_set.all()
            if len(images) > 0:
                context = {}
                context['note'] = note
                context['images'] = images
                context['current_index'] = image_index
                try:
                    context['current_image'] = images[image_index]
                    if image_index + 1 < len(images):
                        context['previous_image'] = images[image_index + 1]
                        context['previous_image_index'] = image_index + 1
                    if image_index - 1 >= 0:
                        context['next_image'] = images[image_index - 1]
                        context['next_image_index'] = image_index - 1
                except IndexError:
                    messages.error(request, ("The image you tried to access does not exist"))
                    return HttpResponseRedirect(reverse('notes:note', args=[pk]))
                context['display_mode'] = DisplayMode.objects.filter(user=default_user)[0].display_mode

                return render(request, 'notes/image_gallery.html', context)
            else:
                messages.error(request, ("The note you tried to access does not have any images"))
                return HttpResponseRedirect(reverse('notes:note', args=[pk]))
        else:
            try:
                note = Note.objects.get(pk=pk)
                messages.error(request, ("You do not have access to this note"))
            except (KeyError, Note.DoesNotExist):
                messages.error(request, ("The note you tried to access does not exist"))
            return redirect('notes:home')


def delete_img(request, pk, image_index, image_pk):
    default_user = User.objects.get(username='te_amo')
    if request.user.is_authenticated:
        try:
            images = Note.objects.get(user=request.user, pk=pk).image_set.all()
            try:
                images.get(pk=image_pk).delete()
                Note.objects.filter(user=request.user, pk=pk).update(last_updated=timezone.now())
            except (KeyError, Image.DoesNotExist):
                messages.error(request, ("The image you tried to delete does not exist"))
        except (KeyError, Note.DoesNotExist):
            try:
                Note.objects.get(pk=pk)
                messages.error(request, ("You do not have access to this note"))
            except (KeyError, Note.DoesNotExist):
                messages.error(request, ("The note you tried to access does not exist")) 
        return HttpResponseRedirect(reverse('notes:note', args=[pk]))
    else:
        try:
            images = Note.objects.get(user=default_user, pk=pk).image_set.all()
            try:
                images.get(pk=image_pk).delete()
                Note.objects.filter(user=default_user, pk=pk).update(last_updated=timezone.now())
            except (KeyError, Image.DoesNotExist):
                messages.error(request, ("The image you tried to delete does not exist"))
        except:
            try:
                Note.objects.get(pk=pk)
                messages.error(request, ("You do not have access to this note"))
            except (KeyError, Note.DoesNotExist):
                messages.error(request, ("The note you tried to access does not exist"))
        return HttpResponseRedirect(reverse('notes:note', args=[pk]))  


def gallery_deletion(index, images):
    """Simulates an image gallery's next item to be shown when one image is deleted"""
    images = list(images)
    new_index = index
    next_images = images[index + 1:]
    previous_images = images[: index]

    try:
        images[index]
    except IndexError:
        print("Didn't work son") # this isnt expected to happen
        sys.exit()
        
    if len(previous_images) > 0:
        new_index = index - 1
    elif len(next_images) > 0:
        new_index = index
    elif [images[index]] == images:
        return None
    
    del images[index]

    return new_index


def delete_img_from_gal(request, pk, image_index, image_pk):
    default_user = User.objects.get(username="te_amo")
    if request.user.is_authenticated:
        note = Note.objects.filter(user=request.user, pk=pk)
        if list(note) != []:
            images = Note.objects.get(user=request.user, pk=pk).image_set.all()
            new_index = gallery_deletion(image_index, images)
            try:
                images.get(pk=image_pk).delete()
                Note.objects.filter(pk=pk).update(last_updated=timezone.now())
                if not(new_index == None):
                    return HttpResponseRedirect(reverse('notes:images', args=[pk, new_index]))
                else:
                    return HttpResponseRedirect(reverse('notes:note', args=[pk]))
            except (KeyError, Image.DoesNotExist):
                images = Note.objects.get(pk=pk).image_set.all()
                try:
                    images.get(pk=image_pk)
                    messages.error(request, ("You do not have access to this image from this account"))
                except (KeyError, Image.DoesNotExist):
                    messages.error(request, ("The image you tried to delete does not exist"))
                return redirect('notes:home')
        else:
            note = Note.objects.filter(pk=pk)
            if list(note) != []:
                messages.error(request, ("You do not have access to this note from this account."))
            else:
                messages.error(request, ("The note you tried to delete does not exist."))
            return redirect('notes:home')
    else:
        note = Note.objects.filter(user=default_user, pk=pk)
        if list(note) != []:
            images = Note.objects.get(user=default_user, pk=pk).image_set.all()
            new_index = gallery_deletion(image_index, images)
            try:
                images.get(pk=image_pk).delete()
                Note.objects.filter(pk=pk).update(last_updated=timezone.now())
                if not(new_index == None):
                    return HttpResponseRedirect(reverse('notes:images', args=[pk, new_index]))
                else:
                    return HttpResponseRedirect(reverse('notes:note', args=[pk]))
            except (KeyError, Image.DoesNotExist):
                images = Note.objects.get(pk=pk).image_set.all()
                try:
                    images.get(pk=image_pk)
                    messages.error(request, ("You do not have access to this image from this account"))
                except (KeyError, Image.DoesNotExist):
                    messages.error(request, ("The image you tried to delete does not exist"))
                return redirect('notes:home')
        else:
            note = Note.objects.filter(pk=pk)
            if list(note) != []:
                messages.error(request, ("You do not have access to this note from this account."))
            else:
                messages.error(request, ("The note you tried to delete does not exist."))
            return redirect('notes:home')


def describe(request, pk, image_index, image_pk):
    current_image = Note.objects.get(pk=pk).image_set.all().filter(pk=image_pk)
    if request.method == "POST":
        new_text = request.POST['alt_text']
        current_image.update(alt_text=new_text)
        return HttpResponseRedirect(reverse('notes:view_image', args=[pk, image_index]))
    else:
        messages.error(request, ('No input was submitted to the form'))
        return redirect('notes:home')