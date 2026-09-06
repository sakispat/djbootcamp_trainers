from django.test import TestCase
from django.urls import reverse
from .models import Trainer


class TrainerViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.trainer = Trainer.objects.create(
            first_name='Nikos',
            last_name='Papadopoulos',
            subject='Python',
        )

    def test_home_displays_trainer(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Papadopoulos')

    def test_create_saves_new_trainer(self):
        count_before = Trainer.objects.count()

        response = self.client.post(
            reverse('create_trainer'),
            {
                'first_name': 'Maria',
                'last_name': 'Georgiou',
                'subject': 'Django',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Trainer.objects.count(),
            count_before + 1,
        )
        self.assertTrue(
            Trainer.objects.filter(
                first_name='Maria',
                last_name='Georgiou',
                subject='Django',
            ).exists()
        )

    def test_empty_form_does_not_create_trainer(self):
        count_before = Trainer.objects.count()

        response = self.client.post(
            reverse('create_trainer'),
            {
                'first_name': '',
                'last_name': '',
                'subject': '',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(
            Trainer.objects.count(),
            count_before,
        )

    def test_update_changes_existing_trainer(self):
        count_before = Trainer.objects.count()

        response = self.client.post(
            reverse('update_trainer', args=[self.trainer.pk]),
            {
                'first_name': 'Nikolaos',
                'last_name': 'Papadopoulos',
                'subject': 'Django',
            },
        )

        self.assertEqual(response.status_code, 302)

        self.trainer.refresh_from_db()

        self.assertEqual(self.trainer.first_name, 'Nikolaos')
        self.assertEqual(self.trainer.subject, 'Django')
        self.assertEqual(
            Trainer.objects.count(),
            count_before,
        )

    def test_delete_get_only_shows_confirmation(self):
        response = self.client.get(
            reverse('delete_trainer', args=[self.trainer.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'trainers/delete_confirm.html',
        )
        self.assertTrue(
            Trainer.objects.filter(pk=self.trainer.pk).exists()
        )

    def test_delete_post_removes_trainer(self):
        response = self.client.post(
            reverse('delete_trainer', args=[self.trainer.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Trainer.objects.filter(pk=self.trainer.pk).exists()
        )