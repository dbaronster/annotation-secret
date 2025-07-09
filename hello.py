import os
import name_module
import output_claude
from pip._vendor.typing_extensions import Self

class Square:
	def __init__(self, side_length):
		self.side_length = side_length
	def area(self):
		return self.side_length * self.side_length


os.system("clear")

test = "now is the time".split(" ")
print (test)
#print(test.len)

print(name_module.namer("Doug"))
#os.system("clear")

my_map = {"one": 1, "two": "too",}

print (my_map)


for x,y in my_map.items():
	print(f"{x}:{y}")


my_square = Square(5)

print(f"Sides: {my_square.side_length}, area is {my_square.area()}")

DOCUMENT_ID = "1eDi9-GSWvmy-_LEpc7hLh9ZnmYXFRGwB"
output_claude.read_google_doc(DOCUMENT_ID)
