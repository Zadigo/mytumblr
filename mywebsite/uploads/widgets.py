from django.forms import widgets


class CustomInput(widgets.Input):
    def get_context(self, name, value, attrs):
        if attrs is None:
            attrs = dict()
        attrs['class'] = 'form-control'
        context = super().get_context(name, value, attrs)
        return context
        

class CustomTextInput(CustomInput):
    template_name = 'widgets/input.html'
    input_type = 'text'


class CustomDateInput(CustomInput):
    template_name = 'widgets/input.html'
    input_type = 'date'


class CustomUrlInput(CustomInput):
    template_name = 'widgets/input.html'
    input_type = 'url'


class CustomSelectInput(widgets.Select):
    template_name = 'widgets/select/select.html'
    option_template_name = 'widgets/select/option.html'

    def get_context(self, name, value, attrs):
        if attrs is None:
            attrs = dict()
        attrs['class'] = 'custom-select'
        context = super().get_context(name, value, attrs)
        return context


class CustomCheckBoxInput(widgets.CheckboxInput):
    template_name = 'widgets/checkbox.html'

    def get_context(self, name, value, attrs):
        if self.check_test(value):
            attrs = {**(attrs or {}), 'checked': True}
        attrs['class'] = 'custom-control-input'
        context = super().get_context(name, value, attrs)
        if '_' in name:
            words = name.split('_')
            label_name = ' '.join(words)
            context['label_name'] = label_name.title()
        else:
            context['label_name'] = name.title()
        return context
