#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from collections import deque
# plots
import plotly.offline as pl
import plotly.graph_objs as go


def linear_pnrg(a, b, m):
	return lambda k: (a * k + b) % (2 ** m)

def register_prng(f):
	def prng(seed):
		new = f(seed)
		seed.popleft()
		seed.append(new)
		return int(''.join(seed), 2) / len(seed)
	return prng


def gen(prng, n, seed, modulus=False):
	i = 0
	seen = []
	while(seed not in seen and i < n):  # and i < 1000000
		# print(seed)
		seen.append(seed)
		seed = prng(seed)
		i += 1

	return seen if not modulus else [x % modulus for x in seen]



def plot(results, filename):

	# Create a trace
	trace = go.Scatter(
		x = [i for i in range(len(results))],
		y = results,
		mode = 'markers'
	)

	data = [trace]

	# Plot and embed in ipython notebook!
	pl.plot(data, filename='{}.html'.format(filename), auto_open=False)


if __name__ == "__main__":
	prng = linear_pnrg(3, 2, 24)
	# uggly way to remove '.' of the timestamp
	seed = 5  # int(''.join(str(time.time()).split('.')))

	res = gen(prng, 1000, seed)
	plot(res, "linear_{}.png".format(len(res)))
	res = gen(prng, 1000, seed, modulus=2)
	plot(res, "linear_{}_mod2.png".format(len(res)))

	seed = deque([1, 1, 1, 1, 1, 1, 1])
	prng = register_prng(
		lambda q: q[2] ^ q[4] ^ q[7]
	)
	# uggly way to remove '.' of the timestamp

	res = gen(prng, 1000, seed)
	plot(res, "linear_{}.png".format(len(res)))
	res = gen(prng, 1000, seed, modulus=2)
	plot(res, "linear_{}_mod2.png".format(len(res)))
