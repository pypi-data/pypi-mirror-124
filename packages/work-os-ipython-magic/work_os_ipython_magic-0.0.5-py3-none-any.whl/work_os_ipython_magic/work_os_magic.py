# See reference for custom IPython magics
# https://ipython.readthedocs.io/en/stable/config/custommagics.html

from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)

from .team_parser import TeamParser

# The class MUST call this class decorator at creation time
@magics_class
class WorkOsMagic(Magics):

    def __init__(self, shell=None,  **kwargs):
        super().__init__(shell=shell, **kwargs)
        self.team_parser = TeamParser()
        self._team_members = []
        # inject our store in user availlable namespace under __mystore
        # name
        shell.user_ns['wos_team_member'] = self._team_members

    @line_magic
    def show_team_members(self, line):
        "line magic for showing team members"
        print(self._team_members)
        return None

    @cell_magic
    def team_members(self, line, cell):
        "Use cell magic to define team members"
        new_team_members = self.team_parser.parse_team_members(cell)
        self._team_members.extend(new_team_members)
        print("Parsed Team Members:")
        print(new_team_members)
        return None

    @line_cell_magic
    def def_team_member(self, line, cell=None):
        "Line of Cell magic that defines a team member %def_team_member and as %%def_team_member"
        if cell is None:
            print("NOT implemented line magic: def_team_member")
            return line
        else:
            print("NOT implemented cell magic: def_team_member")
            return line, cell
