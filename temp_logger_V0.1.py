import utime
import machine
import onewire, ds18x20
import ntptime

def blink_pwm():
    pwm = machine.PWM(machine.Pin(2))
    pwm.duty(512)
    pwm.freq(1)
    
def blink():
    pin = machine.Pin(2, machine.Pin.OUT)
    pin.off()
    utime.sleep_ms(100)
    pin.on()
    utime.sleep_ms(100)
    pin.off()
    utime.sleep_ms(100)
    pin.on()
    
ntptime.host = "pool.ntp.org"

try:
    print('Sync time...')
    ntptime.settime()
    print("Local time after sync: ", str(utime.localtime()))
    blink()
except:
    blink_pwm()
    


# the device is on GPIO12
dat = machine.Pin(12)

# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for devices on the bus
def device():
    roms = ds.scan()
    print('found devices:', roms)
# nr time the temperature
def temp(nr=1):
    roms = ds.scan()
    # loop nr times and print all temperatures
    for i in range(nr):
        print('temperature:', end=' ')
        ds.convert_temp()
        utime.sleep_ms(750)
        for rom in roms:
            print(ds.read_temp(rom), end=' ')
        print()

def read_temp():
    roms = ds.scan()
    ds.convert_temp()
    utime.sleep_ms(750)
    tempC = ds.read_temp(roms[0])
    return tempC

def get_date():
    date = utime.localtime(utime.time() + 3*60*60)
    date_= str(date[2])+"/"+str(date[1])+"/"+str(date[0])
    return date_

def get_time():
    date = utime.localtime(utime.time() + 3*60*60)
    time_= str(date[3])+":"+str(date[4])+":"+str(date[5])
    return time_

def log_tempC():
    #get temperature reading
    a = read_temp()

    #get time
    log_time = get_time()

    #get date
    log_date = get_date()

    #log string
    temp_log=log_date+" "+log_time+" "+ str(a)

    #write log to file
    f = open('data.txt', 'a')
    f.write(temp_log+'\n')
    f.close()

def deep_sleep(msecs):
  #configure RTC.ALARM0 to be able to wake the device
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
  # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
  rtc.alarm(rtc.ALARM0, msecs)
  #put the device to sleep
  machine.deepsleep()




a=get_date()
b=get_time()
c=read_temp()
print("Logging data : " ,a,"      ",b,"      ",c)
log_tempC()
print("Going into deepsleep in 3 seconds...")
utime.sleep(3)
blink()
#deep_sleep(60000)


