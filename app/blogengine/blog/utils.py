from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import *

from django.contrib.auth.mixins import LoginRequiredMixin


class ObjectDetailMixin:
	model = None
	template = None

	def get(self, request, slug):
		obj = get_object_or_404(self.model, slug__iexact=slug)
		return render(request, self.template, context={
			self.model.__name__.lower(): obj, 'admin_object': obj, 'detail': True
		})


class ObjectCreateMixin(LoginRequiredMixin):
	raise_exception = True

	model_form = None
	template = None

	def get(self, request):
		form = self.model_form()
		return render(request, self.template, context={'form': form})

	def post(self, request):
		bound_form = self.model_form(request.POST)

		if bound_form.is_valid():
			new_obj = bound_form.save()
			return redirect(new_obj)
		return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin(LoginRequiredMixin):
	raise_exception = True

	model = None
	model_form = None
	template = None

	def get(self, request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		bound_form = self.model_form(instance=obj)
		return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

	def post(self, request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		bound_form = self.model_form(request.POST, instance=obj)

		if bound_form.is_valid():
			new_obj = bound_form.save()
			return redirect(new_obj)
		return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin(LoginRequiredMixin):
	raise_exception = True

	model = None
	template = None
	redirect_url = None

	def get(self, request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		return render(request, self.template, context={'obj': obj, 'model': self.model.__name__})

	def post(self, request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		obj.delete()
		return redirect(reverse(self.redirect_url))
