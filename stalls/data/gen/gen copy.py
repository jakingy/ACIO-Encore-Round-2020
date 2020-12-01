import random
random.seed(28570679)

import time
from math import ceil, sqrt, log2, gcd

import os
from shutil import copyfile

VALIDATE = False # does a validation check of every case before writing it (does not check subtask constraints yet)
SHUFFLE_EDGES = False # shuffles up edges a bit, 3x slowdown rip, why is random so slow
MINR = 0
MAXS = 1000000
MAXR = 1000000
MINS = 2
MINM = 2
MAXM = int(1e9)
MINC = 0
MAXC = int(1e9)
MINP = 0
MAXP = int(1e9)

def ne(x, M, C):
    return (x * C) % M

def validate(S,R,M,C,ps,edges):
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
            raise Exception("C > MAXP")
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

def write_case(name,st,S,R,M,C,ps,edges):
    name += "-sub%d" % st
    print("Generating", name)
    if VALIDATE:
        validate(S,R,M,C,ps,edges)
    with open(name + ".in", "w") as case_file:
        case_file.write("%d %d %d %d\n" % (S,R,M,C))
        case_file.write("\n".join(map(str, ps)) + '\n')
        if SHUFFLE_EDGES:
            random.shuffle(edges)
            for e in edges: 
                if random.randint(0,1):
                    case_file.write("%d %d\n" % (e[1], e[0]))
                else:
                    case_file.write("%d %d\n" % e)
        else:
            for e in edges: 
                case_file.write("%d %d\n" % e)


def random_ps(S,mn=0,mx=int(1e9)):
    return [random.randint(mn, mx) for i in range(S)]

def smart_ps(S, M, C, edges):
    # all for adjacents:
   
    ps = [-1]*(S+1)
    seen = [0]*(S+1)
    adj = [[]for i in range(S+1)]
    for a,b in edges:
        adj[a].append(b)
        adj[b].append(a)

    for i in range(1, S+1):
        if not seen[i]:
            stck = [i]
            seen[i] = 1
            ps[i] = random.randint(MINP, MAXP)
            while stck: #don't need to do in stack order
                u = stck.pop()
                for v in adj[u]:
                    if not seen[v]:
                        opt = random.randint(0,4)
                        # TODO allow distribution of these options to be different for each case
                        if opt == 0:
                            ps[v] = random.randint(MINP, MAXP)
                        elif opt == 1: #equal: !a || !b, a || b
                            ps[v] = ps[u]
                        elif opt == 2: #ne of v is v, ne(a) == a: x | !a, !x | !a
                            x = int(M / gcd(M, C-1))
                            ps[v] = (x * random.randint(0, 10)) % M
                        elif opt == 3: # v is the ne of u (could do u is ne of v TODO) ne(a) == b: !a | b
                            ps[v] = ne(ps[u], M, C)
                        elif opt == 4: #not equal, but ne is same: ne(a) == ne(b): !a | !b
                            x = int(M / gcd(M, C))
                            ps[v] = (ps[u] + (x * random.randint(1, 10))) % M
                        stck.append(v)
                        seen[v] = 1;
            return ps[1:]
    


def complete_edges(S):
    return [(i,j) for i in range(1, S) for j in range(i+1,S+1)]

def cycle_edges(S):
    return [(i, i+1) for i in range(1,S)] + [(S,1)]

def bipartite_edges(S, R, a=None):
    # colour each node either white or black
    # only connect white node to black nodes and vice versa
    if a == None:
        # print(ceil((S - sqrt(S*S - 4*R))/2), int((S + sqrt(S*S - 4*R))/2)) 
        #print(S, R) 
        a = random.randint(ceil((S - sqrt(S*S - 4*R))/2), int((S + sqrt(S*S - 4*R))/2))       
        # print(a)
    edges = []
    nodes = list(range(1, S+1))
    white = random.sample(nodes, a)
    black = list(set(nodes) - set(white))
    if R > a * (S - a)/2: # dense method
        edges = random.sample([(a,b) for a in white for b in black], R)
    else: # sparse method
        seen = set()
        while len(edges) < R:
            ai = random.choice(white)
            bi = random.choice(black)
            if (ai,bi) in seen or (bi,ai) in seen:
                continue
            seen.add((ai,bi))
            edges.append((ai,bi))
    return edges

def random_edges(S, R):
    edges = []
    if R > S * (S - 1)/4: # dense method
        edges = random.sample(complete_edges(S), R)
    else: # sparse method
        seen = set()
        while len(edges) < R:
            ai = random.randint(1, S)
            bi = random.randint(1, S)
            if ai == bi or (ai,bi) in seen or (bi,ai) in seen:
                continue
            seen.add((ai,bi))
            edges.append((ai,bi))
    return edges

def colour2(u, c, adj, seen, cols, cc, ccnt):
    #assumes graph is 2-colourable, must use stack to prevent stack overflow
    stck = [(u,c)]
    while stck:
        u,c = stck.pop()
        seen[u] = 1
        cols[u] = c
        cc[u] = ccnt
        for v in adj[u]:
            if not seen[v]:
                seen[v] = 1
                stck.append((v,1-c))

# takes a bipartite graph and adds additional edges to make it not bipartite
def make_non_bipartite(S, R, edges):
    if len(edges) == R:
        raise Exception("cannot add edges to make graph non-bipartite")
    seen = [0]*(S+1)
    cols = [0]*(S+1)
    cc = [0]*(S+1)
    ccnt = 0
    adj = [[]for i in range(S+1)]
    for a,b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for i in range(1, S+1):
        if not seen[i]:
            colour2(i, 0, adj, seen, cols, cc, ccnt)
            ccnt += 1

    whites = [[] for i in range(ccnt)]
    blacks = [[] for i in range(ccnt)]
    for i in range(1, S+1):
        if cols[i]:
            whites[cc[i]].append(i)
        else:
            blacks[cc[i]].append(i)
    seen = set()
    while len(edges) < R:
        n = random.randint(1, S)
        c = cc[n]
        if len(whites[c]) > 1 and random.randint(0,1):
            a,b = random.sample(whites[c], 2)
        elif len(blacks[c]) > 1:
            a,b = random.sample(blacks[c], 2)
        if (a,b) in seen or (b,a) in seen:
            continue
        seen.add((a,b))
        edges.append((a,b))
        # print("new_edge", len(edges))


# def shuffle_nodes(ps, edges) 

def density_to_discrete(density, cnt):
    mul = cnt/sum(density)
    split = [int(mul * d) for d in density]
    delta = sum(split)-cnt

    if delta > 0:
        nonzeroes = set(i for i,v in enumerate(split) if v > 0)
        while delta > 0:
            idx = random.sample(nonzeroes, 1)
            if split[idx] > 0:
                split[idx] -= 1
                delta -= 1
                if split[idx] == 0:
                    nonzeroes.remove(idx)
    else:
        while delta < 0:
            idx = random.randrange(0,n)
            split[idx] += 1
            delta += 1

    return split

def random_partition(cnt, n):
    density = [random.uniform(0.0, 1.0)for i in range(n)]
    return density_to_discrete(density, cnt)

#merge two graphs
def merge_edges(edgesA, SA, edgesB, SB):
    edgesA += [(e[0] + SA, e[1] + SA) for e in edgesB]
  

def gen_complete(name,st,S,M,C):
    p = random_ps(S)
    edges = complete_edges(S)
    write_case(name,st,S,int((S*S-S)/2),M,C,p,edges)

def sub1():
    print("Generating subtask 1 cases...")

    start_time = time.time()
    gen_complete("large-M=3", 1, 1413, 3, random.randint(0, int(1e9)))
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    gen_complete("large-M=720", 1, 1414, 720, random.randint(0, int(1e9)))
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    gen_complete("large-M=1409", 1, 1409, 1409, random.randint(0, int(1e9)))
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    gen_complete("large-M=3200", 1, 1414, 3200, random.randint(0, int(1e9)))
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    gen_complete("large-M=8711", 1, 1414, 8711, random.randint(0, int(1e9)))
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    gen_complete("max", 1, 1414, 1000000000, random.randint(0, int(1e9)))
    print("--- %s seconds ---" % (time.time() - start_time))

    S = 1414
    R = int((S*(S-1))/2)
    C = random.randint(2, int(1e7))
    M = 690006469
    ps = [463, 463]
    for i in range(S-2):
        ps.append(ne(ps[-1], M, C))

    # long chain work, begin at end
    start_time = time.time()
    write_case("chain-start", 1, S, R, M, C, ps, complete_edges(S))
    print("--- %s seconds ---" % (time.time() - start_time))
    ps.reverse()

    # long chain work, begin at start
    write_case("chain-end", 1, S, R, M, C, ps, complete_edges(S))

    #random chain
    random.shuffle(ps)
    write_case("chain-random", 1, S, R, M, C, ps, complete_edges(S))

    # long chain break
    ps = [ps[1]] + ps[1:]
    write_case("chain-break", 1, S, R, M, C, ps, complete_edges(S))

    #all doubles
    C = random.randint(2, int(1e7))
    ps = [1, 1]
    while len(ps) < S:
        ps.append(ne(ne(ps[-1], M, C), M, C))
        ps.append(ps[-1])
    random.shuffle(ps)
    write_case("all-doubles", 1, S, R, M, C, ps, complete_edges(S))
    
    #no power use
    C = random.randint(2, int(1e7))
    ps = [71259872]
    while len(ps) < S:
        ps.append(ne(ps[-1], M, C))
    random.shuffle(ps)
    write_case("no-power", 1, S, R, M, C, ps, complete_edges(S))

def print_system(cmd):
    print(cmd)
    os.system(cmd)

def gen_sub2_seed(seed):
    random.seed(seed)
    S = random.randint(2, 16)
    R = random.randint(0, S*(S-1)/2)
    M = random.randint(MINM, MAXM)
    C = random.randint(MINC, MAXC)
    edges = random_edges(S, R)
    ps = smart_ps(S,M,C,edges)
    write_case("seed-%d" % seed, 2, S, R, M, C, ps, edges)

def gen_sub5_seed(seed):
    random.seed(seed)
    S = max(MINS,int(2**(random.random()*log2(MAXS))))
    R = random.randint(MINR, min(S*(S-1)/2,MAXR))
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    # print(S,R)
    ps = random_ps(S)
    edges = random_edges(S, R)
    write_case("seed-%d" % seed, 5, S, R, M, C, ps, edges)

def sub2():
    print("Generating subtask 2 cases...")
    
    # random possible graphs
    # random impossible graphs
    print("Compiling grader and solutions...")
    for st in range(1,5):
        print_system("g++ sol-sub%d.cpp -o sub%d.exe -Wl,--stack,67108864 -O2" % (st,st))
    print_system("g++ sol-full.cpp -o sub5.exe -Wl,--stack,67108864 -O2")
    print_system("g++ simple.cpp -o sub0.exe -Wl,--stack,67108864 -O2")
    print_system("g++ grader.cpp -o grader.exe -Wl,--stack,67108864 -O2")
    #seed = 363
    seed = 6029811
    wa = []
    while not wa:
        seed = (seed * 690006469) % 1000000007
        gen_sub2_seed(seed)
        copyfile("seed-%d-sub2.in" % seed, "spudding.in")
        #print("Testing %d..." % seed)
        ac = []
        wa = []
        for st in range(0,6):         
            os.system("sub%d < spudding.in > spudding.out" % st)
            os.system("grader > grader.out")
            if open("grader.out").read().startswith("AC"):
                ac.append(st)
            else:
                wa.append(st)
            if st == 5:
                ans = open("spudding.out").read()

        if 1:#len(wa) > 2:
            print(seed)
            print("AC:", ac)
            print("WA:", wa)
            print("Ans:", ans.strip())
            print()


    """
    WA: [1, 3, 4]
    355998460
    922610360
    310169056
    777811834
    685416215
    835949562 
    500042371 
    176315714
    152860396
    674070126<-
    295335591
    209095035
    626397710
    35943970
    446041801
    816581470

    848892082 # WA: [4]
    578260280 # WA: [1, 3]
    241325112 # WA: [3]
    573971086 # WA: [1, 4]
    586649021 # WA: [3, 4]
    184965835 # WA: [1]
    800593268 # WA: []
    350409170 # WA: []
    318787127 # WA: []
    """



def sub3():
    print("Generating subtask 3 cases...")

    M = 3
    C = 2

    #odd cycle
    S = 999997
    R = S
    ps = random_ps(S, 1, 2)
    edges = cycle_edges(S)
    write_case("odd-cycle", 3, S, R, M, C, ps, edges)

    #even cycle
    S = 1000000
    R = S
    ps = random_ps(S, 1, 2)
    edges = cycle_edges(S)
    write_case("even-cycle", 3, S, R, M, C, ps, edges)

    #complete bipartite graph
    S = 2000
    R = 1000000
    ps = random_ps(S, 1, 2)
    edges = bipartite_edges(S, R, 1000)
    write_case("complete-bipartite", 3, S, R, M, C, ps, edges)

    #random bipartite graph
    S = 1000000
    R = 1000000
    ps = random_ps(S, 1, 2)
    edges = bipartite_edges(S, R)
    write_case("random-bipartite", 3, S, R, M, C, ps, edges)

    #random non-bipartite
    S = 1000000
    R = 1000000
    ps = random_ps(S, 1, 2)
    edges = bipartite_edges(S, R-50000)
    make_non_bipartite(S, R, edges)
    write_case("random-non-bipartite", 3, S, R, M, C, ps, edges)

    #single edge non-bipartite
    S = 1000000
    R = 1000000
    ps = random_ps(S, 1, 2)
    edges = bipartite_edges(S, R-1)
    make_non_bipartite(S, R, edges)
    write_case("single-conflict-non-bipartite", 3, S, R, M, C, ps, edges)
    
    # random bipartite islands
    S = 0
    edges = []
    for i in range(10000):
        s = random.randint(1,180)
        r = random.randint(0, min(int(s*s/4), 200))
        merge_edges(edges, S, bipartite_edges(s, r), s)
        S += s
    R = len(edges)
    ps = random_ps(S, 1, 2)
    write_case("bipartite-islands", 3, S, R, M, C, ps, edges)

    #single non-bipartite island 
    S = 0
    edges = []
    for i in range(10000):
        s = random.randint(1,180)
        r = random.randint(0, min(int(s*s/4), 200))
        merge_edges(edges, S, bipartite_edges(s, r), s)
        S += s
    merge_edges(edges, S, [(1, 2), (2, 3), (3, 1)], 3)
    S += 3
    R = len(edges)
    ps = random_ps(S, 1, 2)
    write_case("single-non-bipartite-island", 3, S, R, M, C, ps, edges)

    #no connections
    S = 1000000
    R = 0
    ps = random_ps(S, 1, 2)
    edges = []
    write_case("no-connections", 3, S, R, M, C, ps, edges)

def sub4():
    print("Generating subtask 4 cases...")
    # line cases
    # long chain broke
    # long chain work
    # 0 - odd 1s - 0
    # 0 - even 1s - 2
    # 2 - even 1s - 0
    # 2 - 1 or more 1s - 2
    # random possible trees
    # random tree with a 0-0
    # random impossible trees without an obvious 0-0


 
def sub5():
    print("Generating subtask 5 cases...")
    # random possible graphs
    # random impossible graphs
    print("Compiling grader and solutions...")
    for st in range(1,5):
        print_system("g++ sol-sub%d.cpp -o sub%d.exe -Wl,--stack,67108864 -O2" % (st,st))
    print_system("g++ sol-full.cpp -o sub5.exe -Wl,--stack,67108864 -O2")
    print_system("g++ simple.cpp -o sub0.exe -Wl,--stack,67108864 -O2")
    print_system("g++ grader.cpp -o grader.exe -Wl,--stack,67108864 -O2")
    #seed = 363
    seed = 6098581
    for i in range(100):
        seed = (seed * 690006469) % 1000000007
        gen_sub5_seed(seed)
        copyfile("seed-%d-sub5.in" % seed, "spudding.in")
        #print("Testing %d..." % seed)
        ac = []
        wa = []
        for st in range(0,1):         
            os.system("sub%d < spudding.in > spudding.out" % st)
            os.system("grader > grader.out")
            if open("grader.out").read().startswith("AC"):
                ac.append(st)
            else:
                wa.append(st)
            if st ==0:
                ans = open("spudding.out").read()

        if 1:#len(wa) > 2:
            print(seed)
            print("AC:", ac)
            print("WA:", wa)
            print("Ans:", ans.strip()[:10])
            print()
    # 820497049
    """
    WA: [1, 2, 3, 4]
    519449774
    871622099
    991784371
    52732610



    479257278 820497049 # WA: [2]
    682506165 685845730 623384257 772553203 # WA: [2, 3, 4]
    123361461 WA: [1, 2]
    """

MAXS = 100

#sub1()
sub2()
#sub3()
#sub4()
#sub5()