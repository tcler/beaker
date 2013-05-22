"""
bkr group-create: Create a group
================================

.. program:: bkr group-create

Synopsis
--------

| :program:`bkr group-create` [*options*] <group-name>

Description
-----------

Create a new group with the specified name and display name.

Options
-------

.. option:: --ldap

   Populate the members from an LDAP group, specified by <group-name>.

.. option:: --display-name

   Display name of the group.

Common :program:`bkr` options are described in the :ref:`Options
<common-options>` section of :manpage:`bkr(1)`.

Exit status
-----------

Non-zero on error, otherwise zero.

Examples
--------

Create a group with group name, 'mygroup' and display name, 'My Group'::

    bkr group-create --display-name="My Group" mygroup

See also
--------

:manpage:`bkr(1)`
"""

from bkr.client import BeakerCommand

class Group_Create(BeakerCommand):
    """Create a Group"""
    enabled = True

    def options(self):
        self.parser.usage = "%%prog %s [options] <group-name>" % self.normalized_name
        self.parser.add_option(
            "--display-name",
            help="Display name of the group",
        )

        self.parser.add_option(
            "--ldap",
            default=False,
            action="store_true",
            help="Create an LDAP group",
        )

    def run(self, *args, **kwargs):

        if len(args) != 1:
            self.parser.error('Exactly one group name must be specified.')

        group_name = args[0]
        display_name = kwargs.get('display_name', group_name)
        ldap = kwargs.get('ldap', False)

        self.set_hub(**kwargs)
        print self.hub.groups.create(dict(group_name=group_name,
                                          display_name=display_name,
                                          ldap=ldap))