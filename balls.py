"""
In order to draw balls in Thompson's Group F, or any group, you must be able
to solve the word problem. Indeed, these are in fact equivalent conditions.
This file will contain code used for a very specific reason, to solve the
world problem for Thompson's Group F, by using rooted binary trees.
"""


class Tree:
    """This node class is what the tree will be made of"""
    class Node:
        def __init__(self, num = 1, left = 0, right = 0):
           self.num = num
           self.left = left
           self.right = right
        def __repr__(self):
           if self.num == 1:
               return "1"
           else:
               return "(" + str(self.left) + "*" + str(self.right) + ")"
    def __eq__(self, other):
           return str(self) == str(other)
    def __init__(self, root):
        self.root = root
    def __repr__(self):
        return str(self.root)


def string_to_tree(s):
   number_parens = 1

   i = 1
   if len(s) == 1:
      return Tree(Tree.Node())
   while True:
       if s[i] == "*" and number_parens == 1:
           break
       if s[i] == "(":
          number_parens += 1
       elif s[i] == ")":
          number_parens += -1
       i += 1

   left = string_to_tree(s[1:i])
   right = string_to_tree(s[i+1:len(s)-1])
   def get_num(d):
      if d == 0:
          return 1
      else:
         return d.root.num

   return Tree(Tree.Node(get_num(left) + get_num(right), left.root, right.root))


def numberfy(s):
    i = 1
    s_ret = ""
    for j in s:
        if j == "1":
            s_ret += str(i)
            i += 1
        else:
            s_ret += j
    return s_ret

def shared_carot(tree_d, tree_r):
    ds = numberfy(str(tree_d))
    rs = numberfy(str(tree_r))
    def collect_carrots(s):
            ls = [] # [(int, int)]
            j = 0
            while j + 4 < len(s):
               if s[j] == "(" and s[j + 4] == ")":
                   ls.append((s[j + 1], s[j + 3]))
               j += 1
            return ls
    carots_ds = collect_carrots(ds)
    carots_rs = collect_carrots(rs)

    for (a,b) in carots_ds:
        for (c,d) in carots_rs:
            if a == c and b == d:
                return int(a)
    return -1

def prune_two_trees(tree_domain, tree_range):
    def prune_two_trees_i(tree_domain, tree_range, i):
        remove_carot(tree_domain, i)
        remove_carot(tree_range, i)
    ind = shared_carot(tree_domain, tree_range)
    while ind != -1:
        prune_two_trees_i(tree_domain, tree_range, ind)
        ind = shared_carot(tree_domain, tree_range)




def refine(tree, index):
    def refine_root(root, index):
        if index == 0 and root.num == 1:
            root.left = Tree.Node()
            root.right = Tree.Node()
            root.num = 2
            return
        elif index >= root.left.num:
            refine_root(root.right, index - root.left.num)
            root.num += 1
        else:
            refine_root(root.left, index)
            root.num += 1

    refine_root(tree.root, index)

def get_depths(tree):
    """Gets all the depths of the leaves of the tree"""
    def get_depths_root(root):
        if root.num == 1:
            return [0]
        else:
           return [h + 1 for h in
                  (get_depths_root(root.left) + get_depths_root(root.right))]
    return get_depths_root(tree.root)

def remove_carot(tree, lower):
    """This will remove the carot from the tree which has lower as its left side."""
    def remove_carrot_root(root, index):
        if index == 1 and root.left.num == 1:
            root.left = 0
            root.right = 0
            root.num = 1
            return
        elif index >= root.left.num:
            remove_carrot_root(root.right, index - root.left.num)
            root.num += -1
        else:
            remove_carrot_root(root.left, index)
            root.num += -1

    remove_carrot_root(tree.root, lower)

def correct(mx, ds, one, two):
    i = len(ds) - 1

    while i >= 0:
        if ds[i] != mx:
            refine(two, i)
            refine(one, i)
            i += 1
            ds = get_depths(two)
        else:
            i += -1
    return (one, two)

def op(elem, gen):
    """op will take an elem (as a tree diagram) and perform the group
    operation, applying gen on the left.

    Note, this means that the tree diagrams will be:

    gen = (c,d)
    elem = (a,b)
    And  elem +  gen or a -> b > c -> d will be (a', d')

    NOTE: This is not the most efficient algorithm
    """
    (c, d) = gen
    (a, b) = elem
    dsb = get_depths(b)
    dsc = get_depths(c)
    mx = max(dsb + dsc)
    (a, b) = correct(mx, dsb, a, b)
    (d, c) = correct(mx, dsc, d, c)
    prune_two_trees(a,d)
    return (a,d)

a1 = Tree(Tree.Node(3,Tree.Node(), Tree.Node(2, Tree.Node(), Tree.Node())))
a2 = Tree(Tree.Node(3, Tree.Node(2, Tree.Node(), Tree.Node()), Tree.Node()))

A = (string_to_tree(str(a1)), string_to_tree(str(a2)))
A_inv = (string_to_tree(str(a2)), string_to_tree(str(a1)))


b1 = Tree(Tree.Node(4, Tree.Node(), Tree.Node(3, Tree.Node(), Tree.Node(2, Tree.Node(), Tree.Node()))))
b2 = Tree(Tree.Node(4, Tree.Node(), Tree.Node(3, Tree.Node(2, Tree.Node(), Tree.Node()), Tree.Node())))

B = (string_to_tree(str(b1)), string_to_tree(str(b2)))
B_inv = (string_to_tree(str(b2)), string_to_tree(str(b1)))

iden = (Tree(Tree.Node()), Tree(Tree.Node()))


def elem_to_str(elem):
    return str(str(elem[0]) + "+" + str(elem[1]))

def str_to_elem(s):
    spl = s.split("+")
    return (string_to_tree(spl[0]), string_to_tree(spl[1]))



def build_graph(num, graph = {}):
    import json
    js = {}
    if graph == {}:
    	graph = {elem_to_str(iden):{"name": ""}}
    sz = 0
    while sz < num:
        for elem in graph.keys():
            if 'a' not in graph[elem]:
                sz += 1
                elem_t = str_to_elem(elem)
                # Bit of a mix up. The variable A is the generator a
                #                               A_inv is the inverse of a
                # etc
                graph[elem]['a'] = elem_to_str(op(elem_t, str_to_elem(elem_to_str(A))))
                elem_t = str_to_elem(elem)
                graph[elem]['A'] = elem_to_str(op(elem_t, str_to_elem(elem_to_str(A_inv))))
                elem_t = str_to_elem(elem)
                graph[elem]['b'] = elem_to_str(op(elem_t, str_to_elem(elem_to_str(B))))
                elem_t = str_to_elem(elem)
                graph[elem]['B'] = elem_to_str(op(elem_t, str_to_elem(elem_to_str(B_inv))))

                def handle_gen(gen):
			if graph[elem][gen] not in graph:
			    graph[graph[elem][gen]] = {'name': graph[elem]["name"] + gen}
                if graph[elem]['a'] not in graph:
                    graph[graph[elem]['a']] = {'name': graph[elem]["name"] + 'a'}
                if graph[elem]['A'] not in graph:
                    graph[graph[elem]['A']] = {'name': graph[elem]["name"] + 'A'}
                if graph[elem]['B'] not in graph:
                    graph[graph[elem]['B']] =  {'name': graph[elem]["name"] + 'B'}
                if graph[elem]['b'] not in graph:
                    graph[graph[elem]['b']] = {'name': graph[elem]["name"] + 'b'}
    return graph


graph = build_graph(100)
j = 0
grph2 = {}

def swap_case(name):
   return ''.join(c.lower() if c.isupper() else c.upper() for c in name) 

import networkx as nx
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
f = plt.figure()
G = nx.DiGraph()


dct_elem_to_num = {}
i = 0
for key in graph:
       name = graph[key]["name"]
       # changed that to name to make it easier, don't need to fiddle
       dct_elem_to_num[name] = name
       i += 1
       G.add_node(dct_elem_to_num[name])
       print(graph[key]["name"])


a_edges = []
b_edges = []
for key in graph:
   v = graph[key]

   if 'a' in v:
      rt = {"edges":[]}
      j += 1
      #print(v["name"])
      name = v["name"]
      print(name)
      num = dct_elem_to_num[name]
      for k in v:
          if k != "name":
              other_num = dct_elem_to_num[graph[v[k]]["name"]]
              print((num, other_num))
              G.add_edges_from([(num, other_num)])
              if k == 'a' or k == 'A':
                  a_edges.append((num, other_num))
              else:
                  b_edges.append((num, other_num))
              rt["edges"].append(graph[v[k]]["name"])
              rt[k] = graph[v[k]]["name"]
              s  = str((k, graph[v[k]]["name"]))
              #print("    " + s)
   
      grph2[v["name"]] = rt


def position_item(item):
        base = [.5, .5]
        c = .25
        for s in item:
            chn = {'a':[0,c], 'A':[0, -c], 'b':[c, 0], 'B':[-c, 0]}
            base[0] += chn[s][0]
            base[1] += chn[s][1]
            c = c / 2
        return base

def pos_free(pos):

    for key in pos:
        pos[key] =  position_item(key)
    return pos


import random
from math import sin
from math import cos
from math import sqrt
from math import pi
def concentric_circles(pos):
    ordered = sorted(pos.keys(), key=lambda a: len(a))
    def distance_special(p, inner_edge, pos):
        d = 0
        for n in inner_edge:
            np = pos[n]
            x = (p[0] - np[0]) 
            y = (p[1] - np[1])
            d += x * x + y * y
        return d
    for a in ordered:
          print(a)
          base = [.5, .5]
          inner_edge = [e for e in G[a] if len(e) < len(a)]
          print(inner_edge)
          t = 250
          r = random.uniform(0,2 * pi)
          m = len(a) * len(a) * len(a)
          p = [base[0] + sin(r) * m, base[1] + cos(r) * m]
          d = distance_special(p, inner_edge, pos)

          while len(inner_edge) > 0 and t > 0:
               t += -1
               r = random.randint(0,100000)
               n_p = [base[0] + sin(r) * m, base[1] + cos(r) * m]
               dt = distance_special(n_p, inner_edge, pos)
               if dt < d:
                   d = dt
                   p = n_p
          pos[a] = p
          if len(a) <= 3:
              pos[a] = position_item(a)         
    return pos

def draw_graph():
#    pos = {"":(0,0), "a":(1,0), "b":(0,1)}
    pos = nx.spring_layout(G)
    #pos = pos_free(pos)
    for i in range(1,7):
        pos = concentric_circles(pos)
        nx.draw_networkx_nodes(G, pos, node_size=0, width=.1, nodes=[n for n in pos.keys() if len(n) <= i])
        nx.draw_networkx_edges(G, pos, edgelist=a_edges, edge_color='r', arrows=True, width=.1)
        nx.draw_networkx_edges(G, pos, edgelist=b_edges, edge_color='b', arrows=True, width=.1)
        #nx.draw_spring(G, ax=f.add_subplot(111), node_size=100, widths=1, arrows = True)
        f.savefig("graph-" + str(i) + ".png", dpi=2000)

#draw_graph()
"""
for (a,b) in ls:
   if b != "":
       if a == "":
           print("ID")
       else:
           print(a)
       print(b)
"""
