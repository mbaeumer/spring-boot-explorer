from endpoint import Endpoint

def write_csv_file(filename, endpoints):
  try:
    file = open(filename, "w")
    for p in endpoints:
      line = p.rest_controller + "," + p.http_method + "," + p.url + "\n"
      file.write(line)
    file.close()
    print("Finished writing data to file")
  except FileNotFoundError:
    raise FileNotFoundError
