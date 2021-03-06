from __future__ import division
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

import base36
import datetime
from django.utils import timezone

from django.db import connection
from prom.models import promise
from django.contrib.auth.models import User

from .forms import searchForm

class RecordView(View):
	template = 'record.html'

	def get(self, request):
		form = searchForm()
		#assert False, request

		params = {
			'webcrawl': True,
			'form': form,
			'nosearch': True,
		}
		return render(request, self.template, params)

	def post(self, request):
		form = searchForm(request.POST)
		#assert False, request

		if not form.is_valid():
			params = {
				'form': form,
				'nosearch': True
			}
			#assert False, form
			return render(request, self.template, params)

		promorEmail = form.cleaned_data['search']

		cursor = connection.cursor()
		query = '''
			SELECT promid, privacy,
				CASE
					WHEN status = 'draft' THEN 'pending'
					ELSE status
				END status, cdate, mdate,
				CASE
					WHEN char_length(details) >= 30 THEN
						left(details, 30) || '...'
					ELSE
						details
				END details
			FROM promise p
			JOIN auth_user au ON p.promorid_id = au.id
			WHERE au.email = %s
				AND status IN ('broken', 'fulfilled', 'draft')
			ORDER BY mdate desc;'''
		cursor.execute(query, [promorEmail])
		rows = cursor.fetchall()

		# mine data for stats
		fulfilled = 0
		broken = 0
		count = 0
		truthful = 0
		pending = 0
		public = 0

		if rows:
			for row in rows:
				if row[1] == 'public':
					public += 1

				if row[2] == 'fulfilled':
					fulfilled += 1
				elif row[2] == 'broken':
					broken += 1
				elif row[2] == 'pending':
					pending += 1
				count += 1

			if fulfilled or broken:
				truthful = fulfilled / (fulfilled + broken) * 100
				truthful = int(round(truthful))
				#assert False, fulfilled

		params = {
			'form': form,
			'rows': rows,
			'current': timezone.now(),
			'truthful': truthful,
			'fulfilled': fulfilled,
			'broken': broken,
			'pending': pending,
			'public': public,
		}
		return render(request, self.template, params)
