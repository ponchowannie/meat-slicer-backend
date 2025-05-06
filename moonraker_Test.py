from moonrakerpy import MoonrakerPrinter

# Initialize the printer connection
printer = MoonrakerPrinter("http://172.20.10.6")

# List all available printer objects
response = printer.query_status('gcode')['commands']['STATUS']
print(response)
