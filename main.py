from math import log
from itertools import combinations

def dfs_edit(	matrix, 
				start, 
				last_nodes,
				global_paths, local_path, 
				visited=None):
	if visited is None: 
		visited = [True]*len(matrix)

	if start in last_nodes:
		global_paths.append([i for i in local_path])
	
	visited[start] = False
	for col in range(len(matrix[start])):
		if matrix[start][col] == 1 and visited[col]:
			local_path.append(col)
			dfs_edit(matrix, col, last_nodes, global_paths, local_path, visited)
			local_path.remove(col)
	visited[start] = True
	return visited


# 4 v
#		 1  2  3  4  5  6  7  8  9
mtx = [	[0, 0, 1, 1, 0, 0, 0, 0, 0], 	# 1
		[0, 0, 1, 0, 1, 0, 0, 0, 0], 	# 2
		[0, 0, 0, 1, 1, 0, 0, 0, 0], 	# 3
		[0, 0, 0, 0, 0, 0, 1, 1, 0], 	# 4
		[0, 0, 0, 0, 0, 1, 0, 0, 0], 	# 5
		[0, 0, 0, 0, 0, 0, 1, 0, 1], 	# 6
		[0, 0, 0, 0, 0, 0, 0, 1, 1], 	# 7
		[0, 0, 0, 0, 0, 0, 0, 0, 0], 	# 8
		[0, 0, 0, 0, 0, 0, 0, 0, 0]]	# 9
p = [0.88, 0.42, 0.05, 0.62, 0.44, 0.13, 0.22, 0.63, 0.27]
'''
# example
#		 1  2  3  4  5  6  7  8
mtx = [	[0, 1, 1, 0, 0, 0, 0, 0], 	# 1
		[0, 0, 0, 1, 1, 0, 0, 0], 	# 2
		[0, 0, 0, 1, 0, 1, 0, 1], 	# 3
		[0, 0, 0, 0, 1, 1, 0, 1], 	# 4
		[0, 0, 0, 0, 0, 1, 1, 0], 	# 5
		[0, 0, 0, 0, 0, 0, 1, 1], 	# 6
		[0, 0, 0, 0, 0, 0, 0, 0], 	# 7
		[0, 0, 0, 0, 0, 0, 0, 0]]	# 8
p = [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.92, 0.94]
# 22 v
#		 1  2  3  4  5  6  7  8
mtx = [	[0, 1, 1, 0, 0, 0, 0, 0], 	# 1
		[0, 0, 0, 1, 1, 1, 0, 0], 	# 2
		[0, 0, 0, 1, 1, 0, 1, 0], 	# 3
		[0, 0, 0, 0, 1, 1, 1, 0], 	# 4
		[0, 0, 0, 0, 0, 1, 1, 0], 	# 5
		[0, 0, 0, 0, 0, 0, 0, 1], 	# 6
		[0, 0, 0, 0, 0, 0, 0, 1], 	# 7
		[0, 0, 0, 0, 0, 0, 0, 0]]	# 8
p = [0.84, 0.84, 0.91, 0.6, 0.44, 0.74, 0.57, 0.79]
'''

TIME = 10
paths = []

first_nodes = []
last_nodes = []
for i in range(len(mtx)):
	flag_first = True
	flag_last = True
	for j in range(len(mtx)):
		if mtx[j][i] == 1:
			flag_first = False
		if mtx[i][j] == 1:
			flag_last = False
			
	if flag_first:
		first_nodes.append(i)
	if flag_last:
		last_nodes.append(i)

for i in first_nodes:
	dfs_edit(mtx, i, last_nodes, paths, [i])

new_paths = [list(range(len(mtx))), *paths]
for i in paths:
	semi_universal = set(range(len(mtx))) - set(i)
	for j in range(len(semi_universal)):
		for k in combinations(semi_universal, j):
			if sorted(i + list(k)) not in new_paths:
				new_paths.append(sorted(i + list(k)))

new_paths.sort(key=len, reverse=True)

p_paths = []	
for i in new_paths:
	t = 1
	universal = list(range(len(mtx)))
	for j in i:
		t *= p[j]
		universal.remove(j)
	for j in universal:
		t *= 1 - p[j]
	p_paths.append(t)

print("Всі шляхи від 1 до {}:".format(len(mtx)), 
		*["[{:s}]".format(", ".join(map(lambda x: str(x+1), paths[i]))) 
			for i in range(len(paths))], sep="\n")
print("\nТаблиця працездатних станів системи:", 
		*["[{:s}] = {:.10f}".format(", ".join(map(lambda x: str(x+1), new_paths[i])), p_paths[i]) 
			for i in range(len(new_paths))], sep="\n")
print("\nЙмовірність відмови P = {:.10f}".format(sum(p_paths)))
print("Інтенсивність відмов λ = {:.10f}".format(-log(sum(p_paths)) / TIME))
print("Середній наробіток до відмови T = {:.10f}".format(-TIME / log(sum(p_paths))))