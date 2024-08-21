''' Program for the measurement of
temperature dependent IV characteristics of diode
with out the temperature controller
Date: 05/05/2024
'''

# Establish Connection
import eyes17.eyes
p = eyes17.eyes.open()

# Import python libreary 
import time, math
import numpy as np
import threading
import os

# Define the function to mesaure the temperature
def temperature():
    """Function to measure the instanteneous temperature"""
    R0 = 1000                    # PT1000 (RTD Name)
    Alpha = 3.85/1000            # Temperature coefficient 
    n = 1                        # NO of measurements for averaging
    Rsum = 0
    for x in range (0,n):        # Loop for averaging
        r = p.get_resistance()   # Measure the resistance in ohm
        Rsum = Rsum+r            # Sum of resistance
    R = Rsum/n                   # Average resistance
    T = (1/Alpha)*((R/R0)-1)     # Calculate Temperature from Resistance
    return T 


# Define function to show current temperature on screen
def show_temperature():
    while True:
        print("Temperature =","%4.1f" % temperature(), "°C")
        time.sleep(5)
    


#Define the function for IV measurement
def IV():
   """Function to measure IV Characteristics"""
   
   os.system("pause")            # wait till a key is pressed
   Pv1=None                      # Clear Pv1 value
   v=None                        # Clear v value
   
   Pv1 = 0.0                     # Set voltage lower limit
   Start_Temperature = temperature() # Temperature at IV start
   print("Starting Temperature =","%4.1f" % Start_Temperature, "°C")
   while Pv1<=5.0:               # Set voltage upper limit
      p.set_pv1(Pv1)             # Set the voltage at Pv1
      v = p.get_voltage('A1')    # Measured Voltage in volt
      i=(Pv1-v)                  # Measured Current in mA (1K resistor)
      print(v,i)                 # Print V I value on screen
      file = open ("IV.dat ", "a") # Open Appending file
      file.write("{0:2.3f} {1:2.3f}\n".format(v,i)) # Writing data on file
      Pv1 = Pv1+0.1              # Voltage increment
      
   Stop_Temperature = temperature() # Temperature at IV stop
   print("Ending Temperature =","%4.1f" % Stop_Temperature, "°C")
   
   
# Threading all togather for running Concurrently        
if __name__ == "__main__":
    #t1 = threading.Thread(target=Temperature_Controller)
    t1 = threading.Thread(target=show_temperature)
    t2 = threading.Thread(target=IV)
    
    t1.start()
    t2.start()

    t1.join()
    t2.join()










