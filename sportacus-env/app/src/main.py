import spade
import time

class DummyAgent(spade.agent.Agent):
    
    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))



if __name__ == "__main__":
    dummy = DummyAgent("sportacus@arcipelago.ml", "sportacus")
    dummy.start()

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    dummy.stop()