from datetime import datetime, timedelta
from vulnDB.projects.models import Project, VulnInst
from django.shortcuts import get_object_or_404
from vulnDB.vulns.models import Vuln


class ChartData(object):
    @classmethod
    def get_dst_by_severity(cls, project_pk):
        project = get_object_or_404(Project, pk=project_pk)
        vulns = project.vulninst_set.all()
        data = {}
        for v in vulns:
            try:
                data[v.get_severity().severity] += 1
            except KeyError:
                data[v.get_severity().severity] = 1
        jsondata = [[c, data.get(c)] for c in data.keys()]
        return jsondata

    @classmethod
    def get_dst_by_type(cls, project_pk):
        project = get_object_or_404(Project, pk=project_pk)
        vulns = project.vulninst_set.all()
        data = {}
        for v in vulns:
            try:
                data[v.type.type] += 1
            except KeyError:
                data[v.type.type] = 1
        jsondata = [[c, data.get(c)] for c in data.keys()]
        return jsondata

    @classmethod
    def get_dst_by_AP(cls, project_pk):
        project = get_object_or_404(Project, pk=project_pk)
        vulns = project.vulninst_set.all()
        data = {}
        for v in vulns:
            try:
                data[v.get_action_priority().action_priority] += 1
            except KeyError:
                data[v.get_action_priority().action_priority] = 1
        jsondata = [[c, data.get(c)] for c in data.keys()]
        return jsondata


    @classmethod
    def get_dst_by_AC(cls, project_pk):
        project = get_object_or_404(Project, pk=project_pk)
        vulns = project.vulninst_set.all()
        data = {}
        for v in vulns:
            try:
                data[v.action_complexity.action_complexity] += 1
            except KeyError:
                data[v.action_complexity.action_complexity] = 1
        jsondata = [[c, data.get(c)] for c in data.keys()]
        return jsondata


'''
    @classmethod
    def get_level_breakdown(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()

        glucose_level = Glucose.objects.level_breakdown(
            (now - timedelta(days=days)), now, user)

        chart_colors = {
            'Low': 'orange',
            'High': 'red',
            'Within Target': 'green',
            'Other': 'blue'
        }

        data = []
        keyorder = ['Low', 'High', 'Within Target', 'Other']
        for k, v in sorted(glucose_level.items(),
                           key=lambda i: keyorder.index(i[0])):
            data.append({'name': k, 'y': v, 'color': chart_colors[k]})

        return data

    @classmethod
    def get_avg_by_category(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()

        glucose_averages = Glucose.objects.avg_by_category(
            (now - timedelta(days=days)), now, user)

        data = {'categories': [], 'values': []}
        for avg in glucose_averages:
            rounded_value = core_utils.round_value(avg['avg_value'])
            data['values'].append(
                core_utils.glucose_by_unit_setting(user, rounded_value))
            data['categories'].append(avg['category__name'])

        return data

    @classmethod
    def get_avg_by_day(cls, user, days):
        now = datetime.now(tz=user.settings.time_zone).date()

        glucose_averages = Glucose.objects.avg_by_day(
            (now - timedelta(days=days)), now, user)

        data = {'dates': [], 'values': []}
        for avg in glucose_averages:
            rounded_value = core_utils.round_value(avg['avg_value'])
            data['values'].append(
                core_utils.glucose_by_unit_setting(user, rounded_value))
            data['dates'].append(avg['record_date'].strftime('%m/%d'))

        return data
'''
