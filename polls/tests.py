import datetime
from django.test import TestCase
from django.urls import reverse
from .models import Choice, Poll
from .factories import PollFactory

from django.utils import timezone


class PollsTestCase(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(
            question='Sample poll question',
            pub_date=timezone.now(),
            end_date=timezone.now() + datetime.timedelta(days=7)
        )
        self.choice1 = Choice.objects.create(
            poll=self.poll,
            choice_text='Choice 1'
        )
        self.choice2 = Choice.objects.create(
            poll=self.poll,
            choice_text='Choice 2'
        )

    def test_poll_creation(self):
        self.assertEqual(self.poll.choice_set.count(), 2)

    def test_poll_list_view(self):

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        latest_poll_list = response.context['latest_poll_list']
        poll_question_list = [poll.question for poll in latest_poll_list]
        self.assertListEqual(poll_question_list, ['Sample poll question'])

    def test_poll_detail_view(self):
        response = self.client.get(
            reverse('polls:detail', args=(self.poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poll.question)
