from jupyter_client import KernelManager


class KernelOrchestrator():

    def __init__(self):
        self.managers = {}

    def start(self, user_id):

        folder = "./" + str(user_id)
        manager = KernelManager()
        manager.start_kernel(cwd=folder)
        client = manager.blocking_client()
        self.managers[user_id] = {
            'manager': manager,
            'client' : client
        }

    def get_client(self, user_id):

        return self.managers[user_id]['client']

    def complete(self, code, cursor_pos=None):
        pass

    def inspect(self, code, cursor_pos=None, detail_level=0):
        pass

    def execute(self, user_id, command):
        client = self.get_client(user_id)
        output = client.execute_interactive(command, silent=True)
        #print(type(output))
        return output

    def inspect(self, user_id, variable):


        client = self.get_client(user_id)

        message = client.get_iopub_msg(client.inspect(variable))

        while True:
            #faire une boucle jusqu'à ce que ça soit fini
            pass




orchestrator = KernelOrchestrator()
orchestrator.start(2)
o = orchestrator.execute(2, 'a = 3; a')

#print(o)
print(orchestrator.inspect(2, 'a'))