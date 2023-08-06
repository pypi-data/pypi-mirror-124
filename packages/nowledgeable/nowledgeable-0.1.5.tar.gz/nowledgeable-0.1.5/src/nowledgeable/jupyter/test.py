from jupyter_client import KernelManager

km = KernelManager()

km.start_kernel()

kc = km.blocking_client()
#kc.execute("print('coucou')")

print(kc.execute_interactive("a = 'coucou'"))
#reply = kc.get_shell_msg()

#print(reply)

#print(kc.get_stdin_msg())
