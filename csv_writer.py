from endpoint import Endpoint
import datetime

def write_csv_file(endpoints):
    date = datetime.datetime.now()
    time_stamp = date.strftime("%Y-%m-%d-%H-%M-%S")
    filename = "test-" + time_stamp + ".csv"
    try:
        file = open(filename, "w")
        for p in endpoints:
            line = p.rest_controller + "," + p.http_method + "," + p.url + "\n"
            file.write(line)
        file.close()
        print("Finished writing data to file %s", filename)
    except FileNotFoundError:
        raise FileNotFoundError
