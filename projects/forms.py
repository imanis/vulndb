from django import forms
from django.forms.widgets import HiddenInput
from vulnDB.projects.models import *
from vulnDB.vulns.models import Vuln, VulnCategory,  VulnType,  VulnAction_complexity, VulnExploitation_impact, VulnExploitation_complexity
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextFormField
from django.utils.translation import ugettext as _

class ProjectForm(forms.ModelForm):


    project = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    nature = forms.ModelChoiceField(queryset=ProjectNature.objects.all(), empty_label="(choose from the list)")
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="(choose from the list)")

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['nature'].widget.attrs.update({'class' : ' form-control'})
        self.fields['client'].widget.attrs.update({'class' : ' form-control'})

    class Meta:
        model = Project
        fields = [ 'project', 'nature']



class VulnSelectionForm(forms.Form):

    ids = forms.CharField(widget=HiddenInput)





class ProjectVulnForm(forms.ModelForm):

    # Hide Field
    status = forms.CharField(widget=forms.HiddenInput())

    vulnerability = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    description = forms.CharField(widget=CKEditorWidget(config_name='vuln_description'))
    '''affected_item_tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=255,
        required=True,
        help_text='Use spaces to separate the affected items tags')
'''
    category = forms.ModelChoiceField(queryset=VulnCategory.objects.all(), empty_label="(choose from the list)")
    nature = forms.ModelChoiceField(queryset=ProjectNature.objects.all(), empty_label="(choose from the list)")
    type = forms.ModelChoiceField(queryset=VulnType.objects.all(), empty_label="(choose from the list)")
    tags = forms.CharField(widget=forms.Textarea(attrs={'rows':"1",'cols':'50'}),max_length=255,help_text='Add Afected items to this Vulnerability')


    #description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),max_length=4000)
    recommendation = forms.CharField(widget=CKEditorWidget(config_name='vuln_recommendation'))


    exploitation_impact = forms.ModelChoiceField(queryset=ProjectExploitation_impact.objects.all(), empty_label="(choose from the list)")
    exploitation_complexity = forms.ModelChoiceField(queryset=ProjectExploitation_complexity.objects.all(), empty_label="(choose from the list)")
    action_complexity =  forms.ModelChoiceField(queryset=ProjectAction_complexity.objects.all(), empty_label="(choose from the list)")

   # severity =  forms.CharField()
   # action_priority =  forms.CharField()


    class Meta:
        model = VulnInst
        fields = [ 'vulnerability', 'category', 'nature', 'type','description', 'tags' , 'recommendation',
                  'exploitation_impact', 'exploitation_complexity', 'action_complexity']#, 'severity', 'action_priority']


    def __init__(self, *args, **kwargs):
        project_id= kwargs.pop('project')
        super(ProjectVulnForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class' : 'ckeditor'})

        #self.fields['ref'].widget.attrs.update({'class' : 'form-control'})
        self.fields['vulnerability'].widget.attrs.update({'class' : 'form-control'})
      #  self.fields['severity'].widget.attrs.update({'class' : 'form-control'})
        self.fields['type'].widget.attrs.update({'class' : 'form-control'})
        self.fields['nature'].widget.attrs.update({'class' : 'form-control'})

        self.fields['category'].widget.attrs.update({'class' : ' form-control'})
        #self.fields['affected_item_tags'].widget.attrs.update({'class' : 'form-control'})

        self.fields['exploitation_impact'].widget.attrs.update({'class' : 'form-control'})
        self.fields['exploitation_complexity'].widget.attrs.update({'class' : 'form-control'})
        self.fields['action_complexity'].widget.attrs.update({'class' : 'form-control'})
       # self.fields['action_priority'].widget.attrs.update({'class' : 'form-control'})
        self.fields['exploitation_impact'].queryset=ProjectExploitation_impact.objects.filter(project__id=project_id)
        self.fields['exploitation_complexity'].queryset=ProjectExploitation_complexity.objects.filter(project__id=project_id)
        self.fields['action_complexity'].queryset=ProjectAction_complexity.objects.filter(project__id=project_id)




class ClientForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)

    class Meta:
        model = Client
        fields = ['name']



#update to change cssv
class ChangeServityForm(forms.Form):
    severity=forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control','required':'True'}),queryset=ProjectSeverity.objects.all()
        ,empty_label= _("(choose from the list)"))

    def __init__(self,*args, **kwargs):
        project_id= kwargs.pop('project')
        super(ChangeServityForm, self).__init__(*args, **kwargs)
        self.fields['severity'].queryset=ProjectSeverity.objects.filter(project__id=project_id)


class ChangeActionForm(forms.Form):
    action=forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control','required':'True'}),queryset=ProjectAction_priority.objects.all()
        ,empty_label= _("(choose from the list)"))

    def __init__(self,*args, **kwargs):
        project_id= kwargs.pop('project')
        super(ChangeActionForm, self).__init__(*args, **kwargs)
        self.fields['action'].queryset=ProjectAction_priority.objects.filter(project__id=project_id)





#upadte
class ProjectExploitationImpactForm(forms.ModelForm):
    exploitation_impact = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    def save(self,*args, **kwargs):
        project_id= kwargs.pop('project_id')
        project=Project.objects.get(id=project_id)
        color = self.cleaned_data['color']
        exploitation_impact = self.cleaned_data['exploitation_impact']
        instance = ProjectExploitation_impact(project=project,exploitation_impact=exploitation_impact,color=color)
        instance.save()
        return instance

    def update(self,*args, **kwargs):
        id= kwargs.pop('id')
        instance=ProjectExploitation_impact.objects.get(id=id)
        instance.color = self.cleaned_data['color']
        instance.exploitation_impact = self.cleaned_data['exploitation_impact']
        instance.save()
        return instance

    class Meta:
        model = ProjectExploitation_impact
        fields = ['exploitation_impact','color']

class ProjectExploitationComplexityForm(forms.ModelForm):
    exploitation_complexity = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    def save(self,*args, **kwargs):
        project_id= kwargs.pop('project_id')
        project=Project.objects.get(id=project_id)
        color = self.cleaned_data['color']
        exploitation_complexity = self.cleaned_data['exploitation_complexity']
        instance = ProjectExploitation_complexity(project=project,exploitation_complexity=exploitation_complexity,color=color)
        instance.save()
        return instance

    def update(self,*args, **kwargs):
        id= kwargs.pop('id')
        instance=ProjectExploitation_complexity.objects.get(id=id)
        instance.color = self.cleaned_data['color']
        instance.exploitation_complexity = self.cleaned_data['exploitation_complexity']
        instance.save()
        return instance
    class Meta:
        model = ProjectExploitation_complexity
        fields = ['exploitation_complexity','color']


class ProjectSeverityForm(forms.ModelForm):
    severity= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    def save(self,*args, **kwargs):
        project_id= kwargs.pop('project_id')
        project=Project.objects.get(id=project_id)
        color = self.cleaned_data['color']
        severity = self.cleaned_data['severity']
        instance = ProjectSeverity(project=project,severity=severity,color=color)
        instance.save()
        return instance

    def update(self,*args, **kwargs):
        id= kwargs.pop('id')
        instance=ProjectSeverity.objects.get(id=id)
        instance.color = self.cleaned_data['color']
        instance.severity = self.cleaned_data['severity']
        instance.save()
        return instance

    class Meta:
        model = ProjectSeverity
        fields = ['severity','color']


class ProjectActionPriorityForm(forms.ModelForm):
    action_priority= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    def save(self,*args, **kwargs):
        project_id= kwargs.pop('project_id')
        project=Project.objects.get(id=project_id)
        color = self.cleaned_data['color']
        action_priority = self.cleaned_data['action_priority']
        instance = ProjectAction_priority(project=project,action_priority=action_priority,color=color)
        instance.save()
        return instance

    def update(self,*args, **kwargs):
        id= kwargs.pop('id')
        instance=ProjectAction_priority.objects.get(id=id)
        instance.color = self.cleaned_data['color']
        instance.action_priority = self.cleaned_data['action_priority']
        instance.save()
        return instance
    class Meta:
        model = ProjectAction_priority
        fields = ['action_priority','color']

class ProjectActionComplexityForm(forms.ModelForm):
    action_complexity= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    def save(self,*args, **kwargs):
        project_id= kwargs.pop('project_id')
        project=Project.objects.get(id=project_id)
        color = self.cleaned_data['color']
        action_complexity = self.cleaned_data['action_complexity']
        instance = ProjectAction_complexity(project=project,action_complexity=action_complexity,color=color)
        instance.save()
        return instance

    def update(self,*args, **kwargs):
        id= kwargs.pop('id')
        instance=ProjectAction_complexity.objects.get(id=id)
        instance.color = self.cleaned_data['color']
        instance.action_complexity = self.cleaned_data['action_complexity']
        instance.save()
        return instance
    class Meta:
        model = ProjectAction_complexity
        fields = ['action_complexity','color']