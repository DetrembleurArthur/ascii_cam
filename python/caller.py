from sender import send_stream
from receiver import receive_stream
import threading as th
from register import get_contact

caller1 = get_contact(input("your name: "))
send_th = th.Thread(target=lambda: receive_stream(caller1[1], caller1[2]))

caller2 = get_contact(input("your contact's name: "))

receive_th = th.Thread(target=lambda: send_stream(caller2[1], caller2[2]))

receive_th.start()
send_th.start()
