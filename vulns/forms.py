from django import forms
from vulnDB.vulns.models import Vuln, VulnCategory, VulnType, VulnAction_priority, VulnAction_complexity, \
    VulnExploitation_impact, \
    VulnExploitation_complexity, VulnSeverityMatrix, VulnActionPriorityMatrix, VulnSeverity
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import ugettext as _

from vulnDB.projects.models import ProjectNature
from ckeditor.fields import RichTextFormField

# from crispy_forms.helper import FormHelper


class VulnForm(forms.ModelForm):
    # Hide Field
    status = forms.CharField(widget=forms.HiddenInput())

    vulnerability = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=255)
    description = forms.CharField(widget=CKEditorWidget(config_name='vuln_description'))
    tags = forms.CharField(widget=forms.Textarea(attrs={'rows': "1", 'cols': '50'}), max_length=255,
                           help_text=_('Add Afected items to this Vulnerability as tags, at least one tag such as (server switch web)')
                           )

    category = forms.ModelChoiceField(queryset=VulnCategory.objects.all(), empty_label=_("(choose from the list)"))
    #nature = forms.ModelChoiceField(queryset=VulnNature.objects.all(), empty_label=_("(choose from the list)"))
    nature = forms.ModelChoiceField(queryset=ProjectNature.objects.all(), empty_label=_("(choose from the list)"))
    type = forms.ModelChoiceField(queryset=VulnType.objects.all(), empty_label=_("(choose from the list)"))


    #description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),max_length=4000)
    recommendation = forms.CharField(widget=CKEditorWidget(config_name='vuln_recommendation'))

    exploitation_impact = forms.ModelChoiceField(queryset=VulnExploitation_impact.objects.all(),
                                                 empty_label=_("(choose from the list)"))
    exploitation_complexity = forms.ModelChoiceField(queryset=VulnExploitation_complexity.objects.all(),
                                                     empty_label=_("(choose from the list)"))
    action_complexity = forms.ModelChoiceField(queryset=VulnAction_complexity.objects.all(),
                                               empty_label=_("(choose from the list)"))


    # severity =  forms.CharField()
    # action_priority =  forms.CharField()


    class Meta:
        model = Vuln
        fields = ['vulnerability', 'category', 'nature', 'type', 'description', 'tags', 'recommendation',
                  'exploitation_impact', 'exploitation_complexity',
                  'action_complexity']  #, 'severity', 'action_priority']


    def __init__(self, *args, **kwargs):
        super(VulnForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'ckeditor'})

        #self.fields['ref'].widget.attrs.update({'class' : 'form-control'})
        self.fields['vulnerability'].widget.attrs.update({'class': 'form-control'})
        #  self.fields['severity'].widget.attrs.update({'class' : 'form-control'})
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['nature'].widget.attrs.update({'class': 'form-control'})

        self.fields['category'].widget.attrs.update({'class': ' form-control'})
        #self.fields['affected_item_tags'].widget.attrs.update({'class' : 'form-control'})
        #self.fields['tags'].widget.attrs.update({'class' : 'form-control'})

        self.fields['exploitation_impact'].widget.attrs.update({'class': 'form-control'})
        self.fields['exploitation_complexity'].widget.attrs.update({'class': 'form-control'})
        self.fields['action_complexity'].widget.attrs.update({'class': 'form-control'})
        # self.fields['action_priority'].widget.attrs.update({'class' : 'form-control'})

    def clean_tags(self):
        if len(self.cleaned_data['tags']) == 2:
            raise forms.ValidationError(_('Ce champ est obligatoire.'), code='tagsrequired')
        return self.cleaned_data['tags']

class VulnCategoryForm(forms.ModelForm):
    category = forms.CharField(
        max_length=255,
        required=True,
        help_text=_('Add a new category'))

    class Meta:
        model = VulnCategory
        fields = ['category']

    def __init__(self, *args, **kwargs):
        super(VulnCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})

#update
class ChangeServityForm(forms.Form):
    severity = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'required': 'True'}),
                                      queryset=VulnSeverity.objects.all()
                                      , empty_label=_("choose severity"))

class ChangeActionForm(forms.Form):
    action = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'required': 'True'}),
                                    queryset=VulnAction_priority.objects.all()
                                    , empty_label=_("choose priority"))

#upadte
class ExploitationImpactForm(forms.ModelForm):
    exploitation_impact = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
       
    def __init__(self, *args, **kwargs):
        super(ExploitationImpactForm, self).__init__(*args, **kwargs)
        self.fields['exploitation_impact'].widget.attrs.update({'class' : ' form-control'})
    class Meta:
        model = VulnExploitation_impact
        fields = ['exploitation_impact','color']
        
class ExploitationComplexityForm(forms.ModelForm):
    exploitation_complexity = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
       
    def __init__(self, *args, **kwargs):
        super(ExploitationComplexityForm, self).__init__(*args, **kwargs)
        self.fields['exploitation_complexity'].widget.attrs.update({'class' : ' form-control'})
    class Meta:
        model = VulnExploitation_complexity
        fields = ['exploitation_complexity','color']

class SeverityForm(forms.ModelForm):
    severity= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
       
    def __init__(self, *args, **kwargs):
        super(SeverityForm, self).__init__(*args, **kwargs)
        self.fields['severity'].widget.attrs.update({'class' : ' form-control'})
    class Meta:
        model = VulnSeverity
        fields = ['severity','color']

class ActionPriorityForm(forms.ModelForm):
    action_priority= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
       
    def __init__(self, *args, **kwargs):
        super(ActionPriorityForm, self).__init__(*args, **kwargs)
        self.fields['action_priority'].widget.attrs.update({'class' : ' form-control'})
    class Meta:
        model = VulnAction_priority
        fields = ['action_priority','color']

class ActionComplexityForm(forms.ModelForm):
    action_complexity= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
       
    def __init__(self, *args, **kwargs):
        super(ActionComplexityForm, self).__init__(*args, **kwargs)
        self.fields['action_complexity'].widget.attrs.update({'class' : ' form-control'})
    class Meta:
        model = VulnAction_complexity
        fields = ['action_complexity','color']