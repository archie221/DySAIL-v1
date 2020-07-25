from django.apps import AppConfig


class StudentregConfig(AppConfig):
    name = 'studentReg'

    def ready(self):
    	import studentReg.signals