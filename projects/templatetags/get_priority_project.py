from django import template
from vulnDB.projects.models import *
import datetime
register = template.Library()



@register.tag(name="get_priority_project")
def get_priority_project(parser, token):
    argements = token.split_contents()
    if len(argements) != 5:
        raise template.TemplateSyntaxError("%r tag requires a 4argument" % token.contents.split()[0])
    if argements[3] != 'as':
        raise TemplateSyntaxError, "third argument to the get_priority_project tag must be 'as'"
    return SeverityNode(argements[1],argements[2],argements[4])



class SeverityNode(template.Node):
    def __init__(self, action_complexity,severity,varname):
        self.action_complexity = template.Variable(action_complexity)
        self.severity = template.Variable(severity)
        self.varname=varname

    def render(self, context):
        id_action_complexity= self.action_complexity.resolve(context)
        id_severity= self.severity.resolve(context)
        try:
            context[self.varname]=ProjectActionPriorityMatrix.objects.get(action_complexity=id_action_complexity,severity=id_severity)
            return ''
        except ProjectActionPriorityMatrix.DoesNotExist:
            action_complexity=ProjectAction_complexity.objects.get(id=id_action_complexity)
            severity=ProjectSeverity.objects.get(id=id_severity)
            priority_instance,created=ProjectAction_priority.objects.get_or_create(action_priority="Empty")
            severity=ProjectActionPriorityMatrix(action_complexity=action_complexity,severity=severity,action_priority=priority_instance)
            severity.save()
            context[self.varname]=severity
            return ''
