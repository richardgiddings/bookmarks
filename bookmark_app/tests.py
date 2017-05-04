from django.test import TestCase
from . import views
from .models import List, Section, Link
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth

class ViewTests(TestCase):

    def setUp(self):
        User.objects.create_user(username="user1", password="password1", 
                                 email="mail@example.com")
        self.client.login(username="user1", password="password1")

    """
    Home screen
    """

    def test_home(self):
        # check that the home screen displays
        response = self.client.get(
            reverse('bookmarks:home')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_add_list(self):
        # check modify screen title
        response = self.client.get(
            reverse('bookmarks:add_list')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modify.html')
        self.assertContains(response, 'Add list')

        # add a list using post
        response = self.client.post(
            reverse('bookmarks:add_list'),
            data = {
                'title': 'New list', 
                'user': response.context['user']
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # check it has been added to the database
        self.assertQuerysetEqual(response.context['lists'], 
                                 ['<List: New list>'])
        self.assertEqual(List.objects.count(), 1)

        # check that it appears on home screen
        self.assertContains(response, 'New list')

    def test_home_edit_list(self):
        # add a list to edit
        user = auth.get_user(self.client)
        new_list = List.objects.create(title='Edit title', user=user)
        list_id = new_list.pk

        # check modify screen title
        response = self.client.get(
            reverse('bookmarks:edit_list', kwargs={'list_id': list_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modify.html')
        self.assertContains(response, 'Edit list')

        form = response.context['form']
        data = form.initial
        data['title'] = 'Edited title'

        # edit a list using post
        response = self.client.post(
            reverse('bookmarks:edit_list', kwargs={'list_id': list_id}),
            data,
            follow = True
        )

        # check that the change is on database
        self.assertQuerysetEqual(response.context['lists'], 
                                 ['<List: Edited title>'])

        # check that changes appear on home screen
        self.assertNotContains(response, 'Edit title')
        self.assertContains(response, 'Edited title')

    def test_home_delete_list(self):
        # add a list to delete
        user = auth.get_user(self.client)
        the_list = List.objects.create(title='Delete this list', user=user)
        self.assertEqual(List.objects.count(), 1)
        response = self.client.get(
            reverse('bookmarks:home')
        )
        self.assertContains(response, 'Delete this list')

        # add a Section and a Link too so we can see they are all deleted
        the_section = Section.objects.create(title="The section", 
                                             the_list=the_list)
        the_link = Link.objects.create(
            display_text='Link text',
            url='http://www.example.com',
            notes='Some useful notes',
            section=the_section
        )
        self.assertEqual(Section.objects.count(), 1)
        self.assertEqual(Link.objects.count(), 1)

        # delete a list
        response = self.client.post(
            reverse('bookmarks:delete_list'),
            data={'id':the_list.pk},
            follow=True
        )

        # check that list is no longer on database
        # and that associated section and link also deleted
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Section.objects.count(), 0)
        self.assertEqual(Link.objects.count(), 0)

        # check that it no longer exists on home screen
        self.assertNotContains(response, 'Delete this list')

    def test_home_add_section(self):
        # add a list to attach section to
        user = auth.get_user(self.client)
        the_list = List.objects.create(title='List title', user=user)
        list_id = the_list.pk

        # check modify screen title
        response = self.client.get(
            reverse('bookmarks:add_section', kwargs={'list_id':list_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modify.html')
        self.assertContains(response, 'Add section')

        # add a section using post
        response = self.client.post(
            reverse('bookmarks:add_section', kwargs={'list_id':list_id}),
            data={
                'title':'Section for list',
                'the_list':the_list
            },
            follow=True
        )

        # check that it has been added to the database
        self.assertEqual(Section.objects.count(), 1)

        # chek that it appears on the home screen
        self.assertContains(response, 'Section for list')

    """
    Links screen
    """

    def test_links_edit_section(self):
        # add a section to edit
        user = auth.get_user(self.client)
        the_list = List.objects.create(title="The list", user=user)
        the_section = Section.objects.create(title="The section", 
                                             the_list=the_list)

        # check modify screen title
        response = self.client.get(
            reverse('bookmarks:edit_section', 
                    kwargs={'section_id': the_section.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modify.html')
        self.assertContains(response, 'Edit section')

        # edit a section using a post
        form = response.context['form']
        data = form.initial
        data['title'] = 'Edited title'

        response = self.client.post(
            reverse('bookmarks:edit_section', 
                    kwargs={'section_id': the_section.pk}),
            data=data,
            follow=True
        )

        # check that the changes appear on the database
        section = Section.objects.get(pk=the_section.pk)
        self.assertEqual(section.title, 'Edited title')

        # check that links screen shows edited section
        self.assertContains(response, 'Edited title')

    def test_links_delete_section(self):
        # add a section to delete
        user = auth.get_user(self.client)
        the_list = List.objects.create(title="The list", user=user)
        the_section = Section.objects.create(title="The section", 
                                             the_list=the_list)
        self.assertEqual(Section.objects.count(), 1)
        response = self.client.get(
            reverse('bookmarks:links', kwargs={'section_id': the_section.pk})
        )
        self.assertContains(response, 'The section')

        # delete a section
        response = self.client.post(
            reverse('bookmarks:delete_section'),
            data={'id': the_section.pk},
            follow=True
        )

        # check that section no longer appears on database
        self.assertEqual(Section.objects.count(), 0)

        # check that the section no longer appears on links screen
        self.assertNotContains(response, 'The section')

    def test_links_add_link(self):
        # add list and section
        user = auth.get_user(self.client)
        the_list = List.objects.create(title="The list", user=user)
        the_section = Section.objects.create(title="The section", 
                                             the_list=the_list)

        # check modify screen title
        response = self.client.get(
            reverse('bookmarks:add_link', kwargs={'section_id':the_section.pk})
        )
        self.assertContains(response, 'Add link')

        # add a link using a post
        response = self.client.post(
            reverse('bookmarks:add_link', kwargs={'section_id':the_section.pk}),
            data={
                'display_text':'Link text',
                'url':'http://www.example.com',
                'notes':'Some useful notes',
                'section':the_section
            },
            follow=True
        )

        # check that new link appears on the database
        self.assertEqual(Link.objects.count(), 1)

        # check that the new link appears on the links screen
        self.assertContains(response, 'http://www.example.com')

    def test_links_edit_link(self):
        # add list, section and link
        user = auth.get_user(self.client)
        the_list = List.objects.create(title="The list", user=user)
        the_section = Section.objects.create(title="The section", 
                                             the_list=the_list)
        the_link = Link.objects.create(
            display_text='Link text',
            url='http://www.example.com',
            notes='Some useful notes',
            section=the_section
        )

        # check modify screen title
        response = self.client.get(
            reverse('bookmarks:edit_link', kwargs={'link_id':the_link.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modify.html')
        self.assertContains(response, 'Edit link')

        # edit a link using a post
        form = response.context['form']
        data = form.initial
        data['url'] = 'http://www.new-example.com'

        response = self.client.post(
            reverse('bookmarks:edit_link', kwargs={'link_id':the_link.pk}),
            data=data,
            follow=True
        )

        # check that the link is edited on the database
        link = Link.objects.get(pk=the_link.pk)
        self.assertEqual(link.url, 'http://www.new-example.com')

        # check that the edited link appears on the links screen
        self.assertContains(response, 'http://www.new-example.com')

    def test_links_delete_link(self):
        # add list, section and link
        user = auth.get_user(self.client)
        the_list = List.objects.create(title="The list", user=user)
        the_section = Section.objects.create(title="The section", 
                                             the_list=the_list)
        the_link = Link.objects.create(
            display_text='Link text',
            url='http://www.example.com',
            notes='Some useful notes',
            section=the_section
        )
        self.assertEqual(Link.objects.count(), 1)

        # delete a link
        response = self.client.post(
            reverse('bookmarks:delete_link'),
            data={'id':the_link.pk},
            follow=True
        )

        # check that the link is no longer on the database
        self.assertEqual(Link.objects.count(), 0)

        # check that the link no longer appears on the links screen
        self.assertNotContains(response, 'http://www.example.com')