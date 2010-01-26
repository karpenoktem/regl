id = lambda x: x 

def const(x):
	return lambda *args, **kwargs: x

def comp2(f,g):
	return lambda *args, **kwargs: f(g(*args, **kwargs))

def comp(*funcs):
	return compit(funcs)

def compit(it):
	return reduce(comp2, it, id)
