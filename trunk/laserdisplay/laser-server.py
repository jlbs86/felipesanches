from LaserDisplay import *
LD = LaserDisplay()

from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall 
from twisted.internet import reactor

QUAD_BEZ_QUALITY = 8
CUBIC_BEZ_QUALITY = 8

def update_laser (connections):
  LD.start_frame()
  for con in connections:
    for cmd in con.buffered_commands:
      if cmd[0] == "line":
        msg = LD.line_message(int(cmd[1]), int(cmd[2]), int(cmd[3]), int(cmd[4]))
        LD.schedule(msg)
      if cmd[0] == "quadratic":
        msg = LD.quadratic_bezier_message([[int(cmd[1]), int(cmd[2])], [int(cmd[3]), int(cmd[4])], [int(cmd[5]), int(cmd[6])]], QUAD_BEZ_QUALITY)
        LD.schedule(msg)
      if cmd[0] == "cubic":
        msg = LD.cubic_bezier_message([[int(cmd[1]), int(cmd[2])], [int(cmd[3]), int(cmd[4])], [int(cmd[5]), int(cmd[6])], [int(cmd[7]), int(cmd[8])]], CUBIC_BEZ_QUALITY)
        LD.schedule(msg)
      if cmd[0] == "color":
        LD.set_color([int(cmd[1]), int(cmd[2]), int(cmd[3])])
  LD.end_frame()

connections = []
loop = LoopingCall(update_laser, connections)
loop.start(0)

class SendContent(Protocol):
    valid_commands = ["quadratic", "cubic", "line", "color", "show", "quit"]

    def __init__(self):
      connections.append(self)

    def connectionMade(self):
        self.incoming_commands = []
        self.buffered_commands = []
        self.transport.write(self.factory.text)

    def dataReceived(self, data):
        self.transport.write("resposta: "+data)
        cmd = data.split(" ")

        if cmd[0].strip() == "show":
          self.buffered_commands = self.incoming_commands
          self.incoming_commands = []
          return

        if cmd[0].strip() == "quit":
          self.buffered_commands = []
          self.transport.loseConnection()
          return
          
        if cmd[0].strip() in self.valid_commands:
          self.incoming_commands.append(cmd)

class SendContentFactory(Factory):
    protocol = SendContent
    def __init__(self, text=None):
        if text is None:
            text = "\nLaser Display Sharing Server!\nType commands for the laser display:\nValid commands are "+ str(SendContent.valid_commands) +".\n\n"
        self.text = text

reactor.listenTCP(50000, SendContentFactory())
reactor.run()

