#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from collections import deque

# plots
import plotly.offline as pl
import plotly.graph_objs as go


class PRNG(object):
	"""docstring for PRNG."""

	def __init__(self, seed):
		super(PRNG, self).__init__()
		self.seed = seed
		self.seen = []

	def run(self, n, seen=True, modulus=False):
		i, self.seen, self.T = 0, [], 0
		while i < n:
			new = self.gen()
			if new in self.seen:
				if seen: break
			elif not self.T: self.T = i
			self.seen.append(new if not modulus else new % modulus)
			i += 1
		if not self.T: self.T = i
		return self.seen


class LCG(PRNG):
	"""docstring for LCG."""

	def __init__(self, seed, args):
		super(LCG, self).__init__(seed)
		a, b, m = args
		def prng():
			self.seed = (a * self.seed + b) % (2 ** m)
			return self.seed
		self.gen = prng



class LFSR(PRNG):
	"""docstring for LSFR."""

	def __init__(self, seed, func):
		super(LFSR, self).__init__(seed)
		self.func = func
		def prng():
			new = self.func(self.seed)
			self.seed.popleft()
			self.seed.append(new)
			return int(''.join(map(str, seed)), 2) # / pow(2, len(seed))
		self.gen = prng


def plot(results, filename):
	print("[+] {}: period = {}.".format(type(results).__name__, results.T))
	print("    {}.html: {} number(s) generated.\n".format(filename, len(results.seen)))

	# Create a trace
	trace = go.Scatter(
		x = [i for i in range(len(results.seen))],
		y = results.seen,
		mode = 'markers'
	)

	data = [trace]

	# Plot and embed in ipython notebook!
	pl.plot(data, filename='{}.html'.format(filename), auto_open=False)


if __name__ == "__main__":

	print("[+] PRNG demonstration\n")
	### Linear congruential generator
	# based on three parameters, gives a new number using the one provided as
	# seed. In most cases, a timestamp of the system will be used:
	#
	# 	# uggly way to remove '.' of the timestamp
	# 	int(''.join(str(time.time()).split('.')))

	prng = LCG(
		5,
		(3, 2, 24)
	)

	prng.run(1000, seen=False)
	plot(prng, "linear_{}".format(len(prng.seen)))
	prng.run(1000, seen=False, modulus=2)
	plot(prng, "linear_{}_mod2".format(len(prng.seen)))

	### Linear Feedback Shift Register
	# based on three parameters, gives a new number using the one provided as
	# seed. In most cases, a timestamp of the system will be used:
	#
	# 	# uggly way to remove '.' of the timestamp
	# 	int(''.join(str(time.time()).split('.')))

	prng = LFSR(
		deque([1, 0, 1, 1, 0, 0, 1, 0]),
		lambda q: q[2] ^ q[4] ^ q[7]
	)

	prng.run(1000, seen=False)
	plot(prng, "register_{}".format(len(prng.seen)))
	prng.run(1000, seen=False, modulus=2)
	plot(prng, "register_{}_mod2".format(len(prng.seen)))
