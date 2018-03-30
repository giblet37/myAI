"""
        
"""

from module import Module
from intent import ActiveIntent



class Admin(ActiveIntent):

    def __init__(self): 
        # Matches any statement with these words
        super(Admin, self).__init__(intent=['adminVersion','adminRequests'], user=['Greg'])

    def onError(self):
        self.speak('I do not have admin information on that')

    def action(self, intent, objs):
        print(intent)


class AdminModule(Module):

    def __init__(self):
        intent = [Admin()]
        super(AdminModule, self).__init__('admin', intent, enabled=False)
