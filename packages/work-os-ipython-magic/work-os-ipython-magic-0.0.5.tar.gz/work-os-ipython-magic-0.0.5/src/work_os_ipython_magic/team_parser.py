import yaml

# Parse text to team members
class TeamParser(object):
    def __init__(self):
        pass

    def parse_team_members(self, text):
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            print("Team member is not valid YAML: %s" % exc)
            return {}

        
