from gpiozero import MCP3008
import time 

BATTERY_VOLT = 0
MAX_VOLTAGE = 5

class BatteryHealth:
    
    def __init__(self, offset, freq):
        self.battery = MCP3008(channel=BATTERY_VOLT)
        self.offset = offset
        self.poll = freq
        self.stop_polling = False
    
    def get_value(self):
        return self.battery.value * self.offset * 100
    
    def set_offset(self, offset):
        if self.offset == None:
            self.offset = offset

    def start_polling(self, span, infinite = False):
        curr_time = time.time()
        finish = curr_time + span
        
        while (time.time() < finish) or infinite:
            health = self.get_value()
            
            # all the print statements are going to have to be converted to messages
            if (health < 5):
                print("Go home")
            elif (health < 10):
                print("Voltage critically low")
            elif (health < 20):
                print("voltage low")
            else:
                print("Battery as a percent: {}" .format(health))
            
            # Create a listener here for a message because this will live in a thread
            if self.stop_polling == True:
                break
            
            time.sleep(self.poll)
        print("Exited poll")
        
if __name__ == "__main__":
    # print("Hello world, this is the bird feeder")
    bh = BatteryHealth(2, 5)
    bh.start_polling(30, infinite=True)
