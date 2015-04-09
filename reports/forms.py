from django import forms
from vulnDB.reports.models import *
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import ugettext as _
from ckeditor.fields import RichTextFormField
from django.forms import ModelChoiceField

class MyModelChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name

class ReportsForm(forms.ModelForm):

    template = MyModelChoiceField(widget=forms.RadioSelect(
        attrs={'required': 'True'}),
        queryset=ReportTemplate.objects.all(),
        empty_label=None)

    class Meta:
        model = Report

    def __init__(self, *args, **kwargs):
        super(ReportsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['contact'].widget.attrs.update({'class': 'form-control'})
        self.fields['contact'].empty_label = _("(choose from the list)")
        self.fields['create_user'].widget = forms.HiddenInput()

    def update(self, *args, **kwargs):
        id = kwargs.pop('id')
        instance = Report.objects.get(id=id)
        instance.name = self.cleaned_data['name']
        instance.template = self.cleaned_data['template']
        instance.phones = self.cleaned_data['phones']
        instance.save()
        return instance


class ContactForm(forms.ModelForm):

    class Meta:
        model = ReportContact

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phones'].widget.attrs.update({'class': 'form-control'})


class TemplateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['front_cover'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['front_cover'].empty_label = _("(choose from the list)")
        self.fields['header'].widget.attrs.update({'class': 'form-control'})
        self.fields['header'].empty_label = _("(choose from the list)")
        self.fields['footer'].widget.attrs.update({'class': 'form-control'})
        self.fields['footer'].empty_label = _("(choose from the list)")
        self.fields['font'].widget.attrs.update({'class': 'form-control'})
        self.fields['font'].empty_label = _("(choose from the list)")
        self.fields['font_size'].widget.attrs.update({'class': 'form-control'})
        self.fields['font_size'].empty_label = _("(choose from the list)")
        self.fields['create_user'].widget = forms.HiddenInput()
        self.fields['update_date'].widget = forms.HiddenInput()
        self.fields['update_user'].widget = forms.HiddenInput()




    class Meta:
        model = ReportTemplate


class TemplateStandartForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TemplateStandartForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['front_cover'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['front_cover'].empty_label = _("(choose from the list)")
        self.fields['header'].widget.attrs.update({'class': 'form-control'})
        self.fields['header'].empty_label = _("(choose from the list)")
        self.fields['footer'].widget.attrs.update({'class': 'form-control'})
        self.fields['footer'].empty_label = _("(choose from the list)")
        self.fields['font'].widget.attrs.update({'class': 'form-control'})
        self.fields['font'].empty_label = _("(choose from the list)")
        self.fields['font_size'].widget.attrs.update({'class': 'form-control'})
        self.fields['font_size'].empty_label = _("(choose from the list)")
        self.fields['create_user'].widget = forms.HiddenInput()

        self.fields['update_date'].widget = forms.HiddenInput()
        self.fields['update_user'].widget = forms.HiddenInput()

    class Meta:
        model = ReportTemplateStandart

class FontForm(forms.ModelForm):

    class Meta:
        model = TemplateFont

    def __init__(self, *args, **kwargs):
        super(FontForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})


class FrontCoverPageForm(forms.ModelForm):

    class Meta:
        model = TemplateFrontCoverPage

    def __init__(self, *args, **kwargs):
        super(FrontCoverPageForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})


class HeaderForm(forms.ModelForm):



    class Meta:
        model = TemplateHeader

    def __init__(self, *args, **kwargs):
        super(HeaderForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        # self.fields['content'].widget = CKEditorWidget(config_name='vuln_description')
        # self.fields['content'].widget.attrs.update({'class': 'ckeditor'})

class FooterForm(forms.ModelForm):

    class Meta:
        model = TemplateFooter

    def __init__(self, *args, **kwargs):
        super(FooterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        # self.fields['content'].widget = CKEditorWidget(config_name='vuln_description')
        # self.fields['content'].widget.attrs.update({'class': 'ckeditor'})


class FontSizeForm(forms.ModelForm):

    class Meta:
        model = TemplateFontSize

    def __init__(self, *args, **kwargs):
        super(FontSizeForm, self).__init__(*args, **kwargs)
        self.fields['size'].widget.attrs.update({'class': 'form-control'})


class FontSizeForm(forms.ModelForm):

    class Meta:
        model = TemplateFontSize

    def __init__(self, *args, **kwargs):
        super(FontSizeForm, self).__init__(*args, **kwargs)
        self.fields['size'].widget.attrs.update({'class': 'form-control'})
