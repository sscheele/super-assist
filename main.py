i = 1
try:
	while True:
		_ = input()
		print(i)
		i += 1
except EOFError:
	pass
