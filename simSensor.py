from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('127.0.0.1', port=502)
client.connect()

result = client.read_input_registers(address=100, count=1)

if not result.isError():
    temperature = result.registers[0]
    print(f"Temperature: {temperature}*C")
else:
    print("error")

client.close()

