from django.forms import DateInput

class FCDatePickerWidget(DateInput):
    template_name = 'schedule/fc_datepicker.html'