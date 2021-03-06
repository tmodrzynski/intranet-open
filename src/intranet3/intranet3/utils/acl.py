from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS

class Root(object):

    PERMS = (
        ('PERMISSIONS/GROUPS',           ('freelancer', 'employee', 'coordinator', 'sysop', 'scrum master', 'business', 'hr', 'client',)),
        ('can_view_users',               ('A',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_edit_own_profile',         ('A',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_see_own_bugs',             ('A',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  'A',     )),
        ('can_add_timeentry',            ('A',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_justify_wrongtime',        ('A',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_justify_late',             (' ',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_view_presence',            (' ',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_edit_presence',            (' ',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_view_task_pivot',          (' ',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  'A',     )),
        ('can_view_teams',               (' ',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_view_sprints',             (' ',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  'A',     )),
        ('client_stuff',                 (' ',          'A',        ' ',           ' ',     ' ',            ' ',        ' ',  'A',     )),
        ('can_edit_sprints',             (' ',          ' ',        'A',           ' ',     'A',            ' ',        ' ',  ' ',     )),
        ('can_view_clients',             (' ',          ' ',        'A',           ' ',     'A',            ' ',        ' ',  ' ',     )),
        ('can_view_projects',            (' ',          ' ',        'A',           ' ',     'A',            ' ',        ' ',  ' ',     )),
        ('can_edit_clients',             (' ',          ' ',        'A',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_edit_projects',            (' ',          ' ',        'A',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_edit_teams',               (' ',          ' ',        ' ',           ' ',     ' ',            ' ',        'A',  ' ',     )),
        ('hr_stuff',                     (' ',          ' ',        ' ',           ' ',     ' ',            ' ',        'A',  ' ',     )),
        ('can_see_inactive_users',       (' ',          ' ',        ' ',           'A',     ' ',            ' ',        'A',  ' ',     )),
        ('can_edit_users',               (' ',          ' ',        ' ',           ' ',     ' ',            ' ',        'A',  ' ',     )),
        ('can_see_users_times',          (' ',          ' ',        ' ',           ' ',     'A',            'A',        ' ',  ' ',     )),
        ('can_view_time_report',         (' ',          ' ',        ' ',           ' ',     'A',            'A',        ' ',  'A',     )),
        ('can_view_time_client_report',  (' ',          ' ',        ' ',           ' ',     ' ',            'A',        ' ',  ' ',     )),
        ('can_view_project_client_times',(' ',          ' ',        ' ',           ' ',     'A',            ' ',        ' ',  'A',     )),
        ('can_manage_sprint_boards',     (' ',          ' ',        ' ',           ' ',     'A',            ' ',        ' ',  ' ',     )),


        # ADMIN ONLY:
        ('can_edit_config',              (' ',          ' ',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_edit_trackers',            (' ',          ' ',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_delete_projects',          (' ',          ' ',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_delete_clients',           (' ',          ' ',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_edit_users_timeentry',     (' ',          ' ',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
        ('can_add_user_to_group',        (' ',          ' ',        ' ',           ' ',     ' ',            ' ',        ' ',  ' ',     )),
    )
    __acl__ = []

    @staticmethod
    def generate(perms):
        base = [
            (Allow, Authenticated, ('view',)),
            (Allow, 'g:cron', ('cron',)),
            (Allow, 'g:admin', ALL_PERMISSIONS,),
            ]
        groups = perms[0][1]

        perms = perms[1:]

        result = {group: [] for group in groups}
        for perm, checklist in perms:
            for group, check in zip(groups, checklist):
                # perm, group, check
                if check == 'A':
                    result[group].append(perm)
                elif check != ' ':
                    raise Exception('%s not supported' % check)

        dynamic = []
        for group, perms in result.iteritems():
            dynamic.append((Allow, 'g:%s' % group, perms))

        return base + dynamic

    @classmethod
    def to_js(cls):
        """
        Hack to transport permissions to javascript layer.
        Only works with Allow

        """
        result = {}
        for allow, group, perms in cls.__acl__:
            if allow != Allow:
                raise NotImplementedError('%s not implemented' % allow)
            if ':' in group:
                group = group.split(':')[1]
            if perms == ALL_PERMISSIONS:
                perms = ['__ALL__']
            result[group] = perms
        return result

    def __init__(self, request):
        self.request = request

Root.__acl__ = Root.generate(Root.PERMS)
