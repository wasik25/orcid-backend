from django.db import models
import datetime

class LeaveManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset()

	def all_pending_leaves(self):
		return super().get_queryset().filter(status = 'pending').order_by('-created')

	def all_cancel_leaves(self):
		return super().get_queryset().filter(status = 'cancelled').order_by('-created')

	def all_rejected_leaves(self):
		return super().get_queryset().filter(status = 'rejected').order_by('-created')

	def all_approved_leaves(self):
		return super().get_queryset().filter(status = 'approved')

	def current_year_leaves(self):
		return super().get_queryset().filter(startdate__year = datetime.date.today().year)

