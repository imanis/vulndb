from django import template
from vulnDB.projects.models import *
import datetime
register = template.Library()



@register.tag(name="get_severity_project")
def get_severity_project(parser, token):
    argements = token.split_contents()
    if len(argements) != 5:
        raise template.TemplateSyntaxError("%r tag requires a 4argument" % token.contents.split()[0])
    if argements[3] != 'as':
        raise TemplateSyntaxError, "third argument to the get_severity_project tag must be 'as'"
    return SeverityNode(argements[1],argements[2],argements[4])



class SeverityNode(template.Node):
    def __init__(self, op_comlexity,op_level,varname):
        self.op_comlexity = template.Variable(op_comlexity)
        self.op_level = template.Variable(op_level)
        self.varname=varname

    def render(self, context):
        id_op_comlexity= self.op_comlexity.resolve(context)
        id_op_level= self.op_level.resolve(context)
        try:
            context[self.varname]=ProjectSeverityMatrix.objects.get(exploitation_complexity=id_op_comlexity,exploitation_impact=id_op_level)
            return ''
        except ProjectSeverityMatrix.DoesNotExist:
            exploitation_complexity=ProjectExploitation_complexity.objects.get(id=id_op_comlexity)
            exploitation_impact=ProjectExploitation_impact.objects.get(id=id_op_level)
            severity_instance,created=ProjectSeverity.objects.get_or_create(severity="Empty")
            severity=ProjectSeverityMatrix(exploitation_complexity=exploitation_complexity,exploitation_impact=exploitation_impact,severity=severity_instance)
            severity.save()
            context[self.varname]=severity
            return ''
