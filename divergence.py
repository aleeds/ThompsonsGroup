import networkx as nx
import json

with open("graph.json", "r") as f:
    js = json.loads(f.read())


def con(k):
    if k == "":
        return "ID"
    else:
        return k
G = nx.Graph()
for key in js.keys():
    def add(g):
        #G.add_node(con(key)
        G.add_edge(con(key), 
                   con(js[key][g]))
    add('a')
    add('b')
    add('B')
    add('A')

print(nx.shortest_path_length(G, source="ID", target="abAB"))

def get_words(k, js):
   ls = []

   def alen(l):
       if l == "ID":
           return 0
       else:
           return len(l)

   for key in js.keys():
      if alen(key) == k:
          ls.append(con(key))
   return ls

for i in range(0,5):
    wds = get_words(i, js)
    G.remove_nodes_from(wds)
    sphere = get_words(i+1, js)
    p = []
    for source in sphere:
        for target in sphere:
            
            p = max(nx.shortest_path(G, source=source, target=target), p, key= lambda x : len(x))
    print("The " + str(i) + " radius divergence is " + str(len(p) - 1))
    print([str(x) for x in p])
    
def demon_get():
	t = 0
	for i in range(0, 10):
	    ls = get_words(i, js)
	    t += len(ls)
	    print("At sphere " + str(len(ls)))
