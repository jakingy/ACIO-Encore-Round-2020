"""
Interactive Special Spud Stalls Demo

Instructions
- Go to https://algrx.github.io/demo/
- Make sure python is selcted in the bottom left corner
- Copy this code into the editor
- Enter your case in the multi-line string named CASE (you can copy the sample cases included)
- Click the play button under the output canvas

Legend:
    Grey edge - the spud stalls joined by this edge do not sell the same number of potato varieties mod M
    Red edge - the spud stalls joined by this edge sell the same number of potato varieties mod M
    Grey node - the council's powers have not been used on this stall
    Blue node - the council's powers have been used on this stall
    
- You can click on nodes to toggle the use of council's powers on the corresponding stall
- You can zoom in/out, drag the canvas and pull nodes about
- The fixed button will make the graph stick in place
- The goal is to eliminate all red edges or prove this is impossible
"""

# sample 1
# solution: click nodes 1 and 3
CASE = """
6 7 10 5
3
12
2
0
3
5
1 2
1 3
1 5
2 3
2 4
3 6
5 6
"""

# random challenge: what is the maximum number of red edges you can make in each sample case?

# sample 2
# there is no solution for sample 2
"""
3 3 3 2
1
2
1
2 1
2 3 
3 1
"""

# sample 3
# solution: do nothing
"""
5 4 2 1
1
4
1
5
0
2 1
3 2
4 5
2 4
"""

# Here's an interesting case to play around with, it might take a while to load though.
# You will need to shake the nodes around a bit to see the graph properly.
"""
109 258 3 2
2
1
2
1
2
1
1
1
1
2
2
1
1
2
2
2
1
1
1
1
2
2
1
2
2
1
2
1
1
1
2
1
1
1
2
2
2
1
2
2
2
1
1
1
1
2
2
1
2
2
1
1
2
1
2
1
1
1
1
1
2
2
1
1
2
2
2
2
1
2
2
1
2
1
1
2
1
1
1
2
2
1
2
1
1
2
1
1
2
2
2
2
2
2
1
1
2
2
1
1
2
1
1
1
1
2
2
2
1
19 17
16 11
15 1
2 18
5 20
21 18
9 12
13 14
22 1
4 14
5 12
3 20
3 18
4 7
3 12
10 1
2 20
2 1
21 12
2 14
5 18
15 7
9 14
10 20
6 14
16 14
4 12
2 17
2 11
15 11
26 34
33 32
27 34
27 31
26 23
25 34
26 30
33 23
26 28
29 28
33 31
26 32
29 23
33 28
27 30
29 31
25 31
26 31
29 24
27 23
25 24
27 28
25 23
29 34
25 28
27 24
29 32
26 24
27 32
29 30
33 30
33 34
25 32
33 24
38 39
47 49
44 36
38 41
43 41
55 59
56 59
40 39
42 37
55 36
57 59
46 39
45 37
60 36
48 36
45 41
38 36
60 59
50 39
56 37
60 41
42 39
53 41
44 41
40 59
35 41
47 41
48 59
45 39
60 49
55 41
47 36
60 52
35 52
47 37
62 59
58 36
40 49
58 59
46 41
42 52
45 52
38 49
53 52
55 37
51 39
57 36
44 59
50 41
50 37
43 37
54 52
46 52
62 36
44 49
56 36
60 37
62 49
47 59
43 52
57 49
54 36
43 59
53 59
46 37
45 59
45 36
50 49
44 37
57 52
51 49
53 39
61 52
62 37
51 52
40 41
51 37
50 52
54 37
43 36
44 39
54 59
56 49
57 37
35 39
46 59
53 37
61 41
58 37
43 39
48 49
38 59
35 49
42 36
46 36
55 52
61 59
58 41
54 41
35 36
35 37
62 41
58 52
50 59
58 49
42 41
40 36
48 39
62 52
45 49
40 52
40 37
51 59
48 52
48 37
46 49
55 49
75 72
64 66
77 66
82 66
70 85
79 65
82 85
71 66
78 72
71 72
73 66
84 63
71 63
83 65
78 63
68 65
75 63
83 85
64 85
82 72
69 72
67 63
76 63
73 72
70 65
67 85
77 72
73 65
84 72
74 65
83 63
83 66
80 65
67 72
69 66
73 85
70 72
64 63
64 65
81 65
74 85
78 65
84 65
70 63
74 66
76 72
79 72
79 85
75 66
80 72
79 66
78 85
81 63
77 63
67 65
74 72
81 72
97 103
105 102
86 102
88 102
95 102
89 101
107 101
99 102
93 101
95 101
106 101
96 101
99 103
94 103
86 103
96 102
88 103
87 101
98 103
94 101
"""

MINR = 0
MAXR = 500 # you really don't want more than 500 edges/nodes unless you have a supercomputer
MAXS = 500
MINS = 2
MINM = 2
MAXM = int(1e9)
MINC = 0
MAXC = int(1e9)
MINP = 0
MAXP = int(1e9)

def validate(S,R,M,C,ps,edges):
    #lmao just use asserts
    if S < MINS:
        raise Exception("S < MINS")
    if S > MAXS:
        raise Exception("S > MAXS")
    if R < MINR:
        raise Exception("R < MINR")
    if R > MAXR:
        raise Exception("R > MAXR")
    if M < MINM:
        raise Exception("M < MINM")
    if M > MAXM:
        raise Exception("M > MAXM")
    if C < MINC:
        raise Exception("C < MINC")
    if C > MAXC:
        raise Exception("C > MAXC")
    if len(ps) != S:
        raise Exception("len(ps) != S")
    if len(edges) != R:
        raise Exception("len(edges) != R")
    for p in ps:
        if p < MINP:
            raise Exception("p < MINP")
        if p > MAXP:
            raise Exception("p > MAXP")
    seen = set()
    for e in edges:
        if e[0] < 1:
            raise Exception("ai < 1")
        if e[0] > S:
            raise Exception("ai > S")
        if e[1] < 1:
            raise Exception("bi < 1")
        if e[1] > S:
            raise Exception("bi > S")
        if e[0] == e[1]:
            raise Exception("ai = bi")
        if e in seen or (e[1], e[0]) in seen:
            raise Exception("duplicate edge")
        seen.add(e)
        
def power(x):
    return x * C
    
def recalc_conflict():
    for e in range(R):
        a,b = edges[e]
        nc = 0
        if powps[a] % M == powps[b] % M:
            nc = 1
        else:
            nc = 0
        if nc != conflict[e]:
            if nc:
                canvas.edge((a,b)).color('red').highlight(0).thickness(6)
            else:
                canvas.edge((a,b)).color('grey').highlight(0).thickness(6)
            conflict[e] = nc
        
def use_power(n):
    powps[n] = power(ps[n])
    canvas.node(n).onclick(remove_power).label(1).text(str(powps[n]))
    canvas.node(n).color('blue').highlight(0).size('1.2x')
    recalc_conflict()
    
def remove_power(n):
    powps[n] = ps[n]
    canvas.node(n).onclick(use_power).label(1).text(str(powps[n]))
    canvas.node(n).color('darkgrey').highlight(0).size('1.2x')
    recalc_conflict()
    
def make_fixed(n):
    canvas.node(n).color('blue') # .onclick(make_unfixed) for some reason this doesn't work :(
    canvas.nodes(nodes).fixed(True)
    
#def make_unfixed(n):
#    canvas.node(n).onclick(make_fixed).color('darkgrey')
#    canvas.nodes(nodes).fixed(False)
    
ints = list(map(int,CASE.split()))
S,R,M,C = ints[:4]
ps = ints[4:4+S]
edges = [tuple(ints[i:i+2]) for i in range(4+S, len(ints), 2)]
validate(S,R,M,C,ps,edges)
ps = [0] + ps
powps = ps.copy()
conflict = [-1] * R

nodes = list(range(1, S+1))

canvas.nodes(nodes).add().onclick(use_power)
canvas.edges(edges).add().color('lightblue')#.thickness(3)
canvas.label(1).text("S: %d" % S).pos(("-0.85cx", "0.85cy"))
canvas.label(2).text("R: %d" % R).pos(("-0.85cx", "0.75cy"))
canvas.label(3).text("M: %d" % M).pos(("-0.85cx", "0.65cy"))
canvas.label(4).text("C: %d" % C).pos(("-0.85cx", "0.55cy"))

for n in nodes:
    canvas.node(n).label(1).text(str(powps[n]))

canvas.node(S+1).add(
    pos=("-0.85cx", "0.45cy"),
    shape='rect',
    size=(40, 12),
    fixed=True,
    draggable=False,
    labels={0:{'text': "fixed"}},
).onclick(make_fixed)
    
recalc_conflict()

# Random challenge: move the fixed button to the bottom-right of the screen without zooming or panning. Be warned: the controls are reliably buggy.