# Imports
import os
import time
from datetime import datetime
from sense_hat import SenseHat
import argparse

def exit_pi(sense):
    print('Closing...')
    #sense.set_pixels(zero)
    sense.show_message('bye!')
    sense.clear()


def get_cpu_temp():
    temp = os.popen('/opt/vc/bin/vcgencmd measure_temp')
    cputemp = temp.read()
    cputemp = cputemp.replace('temp=', '')
    cputemp = cputemp.replace('\'C\n', '')
    return float(cputemp)


# not really used now
def get_temp(sense):
    # alternative way of measure the temperature - in theory should reduce the CPU noise.
    temp = sense.get_temperature()
    newtemp = temp - ((get_cpu_temp() - temp) / 2)
    return newtemp


def measure(sense):
    humidity = sense.get_humidity()
    cpu_temp = get_cpu_temp()
    temp = sense.get_temperature()
    pressure = sense.get_pressure()
    timestamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())

    # show comment on pi
    sense.show_message('Temperature: {0}'.format(temp))

    # temperatures
    append_to_file('data/temperature.csv', '{0}, {1}, {2}'.format(timestamp, temp, cpu_temp), 'date, temperature, cpu temperature')

    # humidity
    append_to_file('data/humidity.csv', '{0}, {1}'.format(timestamp, humidity), 'date, humidity')

    # pressure
    append_to_file('data/pressure.csv', '{0}, {1}'.format(timestamp, pressure), 'date, pressure')


def append_to_file(filename, line, headers):
    # if file doesn't exist - add headers before adding the line
    add_headers = not os.path.exists(filename)

    file = open(filename, 'a')

    if add_headers:
        file.write(headers + '\n')

    file.write(line + '\n')
    file.close()


def indicate_measurement(sense, iteration):
    sense.clear()
    sense.set_pixel(iteration%8, iteration%8, 0, 0, 255)

def main():
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--single', help='Changes the execution mode to a single run.', action='store_true')
    parser.add_argument('-i', '--interval', help='Interval for measurements in seconds.', type=int)
    parser.add_argument('-m', '--max', help='Maximum number of iterations.', type=int)
    args = parser.parse_args()

    interval = 600 # 10 min
    max_iterations = 0

    # override interval
    if args.interval and args.interval > 0:
        interval = args.interval

    # override default max value
    if args.max and args.max > 0:
        max_iterations = args.max

    #return


    sense = SenseHat()
    sense.low_light = True

    if args.single:
        print('Running a single measurement.')

        measure(sense)

    elif max_iterations == 0:
        print('No max iterations was chosen - runing in infinite loop.')

        i = 0
        while True:
            indicate_measurement(sense, i)
            i += 1

            measure(sense)
            time.sleep(interval)

    else:
        print('Max iterations was chosen - runing a limited number of iterations.')

        for i in range(0, max_iterations):
            indicate_measurement(sense, i)

            print('Measurement {} of {}. {} left.'.format(i + 1, max_iterations, max_iterations - i - 1))
            measure(sense)
            time.sleep(interval)

    exit_pi(sense)


main()
