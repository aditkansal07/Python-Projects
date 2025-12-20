from pybricks.hubs import PrimeHub          
from pybricks.parameters import Port, Color
from pybricks.pupdevices import Light
from pybricks.tools import wait, StopWatch

# --- Hub & devices ---
hub = PrimeHub()                             
lights = [
    Light(Port.A),
    Light(Port.B),
    Light(Port.C),
    Light(Port.D)
]

def all_on(brightness=100):
    for led in lights:
        led.on(brightness)

def all_off():
    for led in lights:
        led.off()
clock = StopWatch()

# --- Settings ---
ALARM_MS = 5_000     # flash/beep for 5 seconds
TRIGGER  = 1.9        
ALPHA    = 0.98       
BLINK_MS = 250        
BEEP_ON  = True       
BEEP_HZ  = 1200       
BEEP_MS  = 120        

# --- State ---
def mag(x, y, z): return (x*x + y*y + z*z) ** 0.5
prev_m = mag(*hub.imu.acceleration())
hp = 0.0
alarm_until = -1
last_toggle = 0
is_on = False

all_on()
all_off()

while True:
    # --- Vibration detection (high-pass on accel magnitude) ---
    ax, ay, az = hub.imu.acceleration()
    m = mag(ax, ay, az)
    hp = ALPHA * (hp + (m - prev_m))
    prev_m = m
    level = abs(hp)

    now = clock.time()

    if level > TRIGGER:
        # extend alarm window to a full minute from the latest hit
        alarm_until = now + ALARM_MS

    # --- Flash + beep during alarm window ---
    if now < alarm_until:
        if now - last_toggle >= BLINK_MS:
            is_on = not is_on
            last_toggle = now

            if is_on:
                all_on()
                if BEEP_ON:
                    # PrimeHub has a speaker; EssentialHub does not
                    try:
                        hub.speaker.beep(BEEP_HZ, BEEP_MS)
                    except:
                        pass
            else:
                all_off()

    else:
        is_on = False
         all_off()

    wait(10)
