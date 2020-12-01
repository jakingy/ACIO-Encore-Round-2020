import random
from math import ceil, sqrt, log2, gcd
from shutil import copyfile
import time
import os
import treegen
import heapq

SEED = 28570679
random.seed(SEED)

VALIDATE = False # does a validation check of every case before writing it (does not check subtask constraints yet)
SHUFFLE_EDGES = False # shuffles up edges a bit, 3x slowdown rip, why is random so slow
RUN_CASES = False # runs each case on all 6 solutions and gives a list of wa and ac
MINR = 0
MAXR = 1000000
MAXS = 1000000
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

def write_case(name,st,S,R,M,C,ps,edges):
    fname = name + "-sub%d.in" % st
    print("Generating", name)
    if VALIDATE:
        validate(S,R,M,C,ps,edges)
    with open(fname, "w") as case_file:
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
    if RUN_CASES:
        test_case(fname)


def random_ps(S,mn=0,mx=int(1e9)):
    return [random.randint(mn, mx) for i in range(S)]

def attempt_set(ps, x, val, used, S, M, C, adj, force_valid):
    """if ps[x] != -1:
        raise Exception("arleady has ps")
    if x == 30452:  print("setting %d to %d" % (x, val))"""
    ps[x] = val
    #set to -1 if invalid
    if force_valid:
        tused = []
        lvl = 0 # iterations adapt to how active this is
        IT = 5
        while IT:
            IT -= 1
            # if x == 30452:  print("new it")
            inq = set()
            q = []
            qt = set()
            valid = True
            for v in adj[x]:
                psv = ps[v] % M
                if used[v]: psv = ne(psv, M, C)
                if psv == val % M:
                    if x not in inq:
                        heapq.heappush(q, (random.random(), x))
                        inq.add(x)
                    if not used[v]:
                        heapq.heappush(q, (random.random(), v))
                        inq.add(v)
            while len(q):
                if lvl < 5 and len(q) > (1<<(lvl+1)):
                    #print(lvl)
                    lvl += 1
                    IT += 5*(2**lvl)

                pri,u = heapq.heappop(q)
                # if x == 30452: print(u)
                inq.remove(u)
                psu = ps[u] % M
                for v in adj[u]:
                    psv = ps[v] % M
                    if used[v]: psv = ne(psv, M, C)
                    if psu == psv:
                        psu = ne(psu, M, C)
                        tused.append(u)
                        used[u] = 1
                        # if x == 30452:  print("used", u, "ps:", psu)
                        break

                for v in adj[u]:
                    psv = ps[v] % M
                    if used[v]: psv = ne(psv, M, C)
                    if psu == psv and (v not in inq):
                        if not used[v]:
                            inq.add(v)
                            heapq.heappush(q,(random.random(),v))
                            qt.add(v)
                        else:
                            valid = False
                            break
                if not valid:
                    break

            if valid:
                """for u in qt:
                    for v in adj[u]:
                        psu = ps[u]
                        if used[u]: psu = ne(psu, M, C)
                        psv = ps[v]
                        if used[v]: psv = ne(psv, M, C)
                        if psv == psu:
                            print(used[u], used[v])
                            print(psu, psv)
                            print(u)
                            print(adj[u])
                            raise Exception("brokee")"""
                """for v in adj[x]:
                    psx = ps[x]
                    if used[x]: psx = ne(psx, M, C)
                    psv = ps[v]
                    if used[v]: psv = ne(psv, M, C)
                    if psv == psx:
                        print(used[x], used[v])
                        print(psx, psv)
                        print(x)
                        print(adj[x])
                        raise Exception("brokee")"""
                #print("fine")
                return
            while tused:
                used[tused.pop()] = 0
        ps[x] = -1
                            


#force_valid may not be possible given some combinations of edges, M and C
def smart_ps(S, M, C, edges, force_valid = False):
    # all for adjacents:
   
    ps = [-1]*(S+1)
    seen = [0]*(S+1)
    used = [0]*(S+1)
    adj = [[]for i in range(S+1)]
    for a,b in edges:
        adj[a].append(b)
        adj[b].append(a)

    probs = [random.random()for i in range(6)]
    #print(probs)
    psum = sum(probs)

    for i in range(1, S+1):
        if not seen[i]:
            stck = [i]
            seen[i] = 1
            ps[i] = random.randint(MINP, MAXP)
            #attempt_set(ps, i, random.randint(MINP, MAXP), used, S, M, C, adj, force_valid)
            #if ps[i] == -1:
            #    raise Exception("brokee")
            while stck: #don't need to do in stack order
                u = stck.pop()
                for v in adj[u]:
                    if not seen[v]:
                        it = 0
                        while ps[v] == -1:
                            it += 1
                            if it == 501: #break after 500 incase this is actually impossible
                                raise Exception("could not guarantee validity")
                            rng = random.random()*psum
                            for i in range(6):
                                if rng < probs[i]:
                                    opt = i
                                    break
                                else:
                                    rng -= probs[i]
                            #opt = random.randint(0,4)

                            if opt == 0:
                                attempt_set(ps, v, random.randint(MINP, MAXP), used, S, M, C, adj, force_valid)
                                #ps[v] = random.randint(MINP, MAXP)
                            elif opt == 1: #equal: !a || !b, a || b
                                #ps[v] = ps[u]
                                attempt_set(ps, v, ps[u], used, S, M, C, adj, force_valid)
                            elif opt == 2: #ne of v is v, ne(a) == a: x | !a, !x | !a
                                x = int(M / gcd(M, C-1))
                                #ps[v] = (x * random.randint(1, 10)) % M
                                attempt_set(ps, v, (x * random.randint(1, 10)) % M, used, S, M, C, adj, force_valid)
                            elif opt == 3: # v is the ne of u (could do u is ne of v TODO) ne(a) == b: !a | b
                                #ps[v] = ne(ps[u], M, C)
                                attempt_set(ps, v, ne(ps[u], M, C), used, S, M, C, adj, force_valid)
                            elif opt == 4: #not equal, but ne is same: ne(a) == ne(b): !a | !b
                                x = int(M / gcd(M, C))
                                #ps[v] = (ps[u] + (x * random.randint(1, 10))) % M
                                attempt_set(ps, v, (ps[u] + (x * random.randint(1, 10))) % M, used, S, M, C, adj, force_valid)
                            elif opt == 5: #zero
                                #ps[v] = 0
                                attempt_set(ps, v, 0, used, S, M, C, adj, force_valid)
                            else:
                                raise Exception("invalid opt")
                        stck.append(v)
                        seen[v] = 1
    """power = [i for i in range(1, S+1) if used[i]]
    ud = open("used_dump.out","w")
    ud.write("%d\n" % len(power))
    ud.write(" ".join(map(str, power)))
    ud.close() # this is a solution in theory (only works if force_valid is on)"""
    return ps[1:]

def complete_edges(S):
    return [(i,j) for i in range(1, S) for j in range(i+1,S+1)]

def line_edges(S):
    return [(i, i+1) for i in range(1,S)]

def cycle_edges(S):
    return line_edges(S) + [(S,1)]

def tree_to_edges(tree):
    edges = []
    cnt = 1
    tree.id = 1
    stck = [tree]
    while stck:
        u = stck.pop()
        for v in u.child:
            cnt += 1
            v.id = cnt
            stck.append(v)
            edges.append((u.id, v.id))
    return edges

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
    stck = [u]
    seen[u] = 1
    while stck:
        u = stck.pop()
        cc[u] = ccnt
        for v in adj[u]:
            if not seen[v]:
                seen[v] = 1
                cols[v] = 1-cols[u]
                stck.append(v)
            elif cols[v] == cols[u]:
                raise Exception("Graph is not two colourable")

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
    #es = set(edges)
    while len(edges) < R:
        n = random.randint(1, S)
        c = cc[n]
        if len(whites[c]) > 1 and random.randint(0,1):
            a,b = random.sample(whites[c], 2)
        elif len(blacks[c]) > 1:
            a,b = random.sample(blacks[c], 2)
        else:
            continue
        if (a,b) in seen or (b,a) in seen:
            continue
        #if (a,b) in es or (b,a) in es:
        #    raise Exception("bad edge existed before???")
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

COMPILED = False
def test_case(fname):
    global COMPILED
    if not COMPILED:
        print("First test - compiling grader and solutions...")
        for st in range(1,5):
            print_system("g++ ../solutions/sol-sub%d.cpp -o sub%d.exe -Wl,--stack,536870912 -O2" % (st,st))
        print_system("g++ ../solutions/sol-full.cpp -o sub5.exe -Wl,--stack,536870912 -O2")
        print_system("g++ ../solutions/random.cpp -o sub0.exe -Wl,--stack,536870912 -O2")
        print_system("g++ ../checker/checker.cpp -o checker.exe -Wl,--stack,536870912 -O2")
        #print_system("g++ ../checker/checker-old.cpp -o grader.exe -Wl,--stack,536870912 -O2")
        COMPILED = True

    copyfile(fname, "stalls.in")

    print("Testing %s" % fname)
    ac = []
    wa = []
    os.system("sub5 < stalls.in > soln.out")
    for st in range(0,6):         
        os.system("sub%d < stalls.in > stalls.out" % st)
        #os.system("grader > grader.out")
        os.system("checker stalls.in soln.out stalls.out > checker.out")
        if open("checker.out").read().startswith("100"):
            #if not open("grader.out").read().startswith("100"):
            #    raise Exception("Does not match")
            ac.append(st)
        else:
            #if open("grader.out").read().startswith("100"):
            #    raise Exception("Does not match")
            wa.append(st)
        if st == 5:
            ans = open("stalls.out").read()

    #print(seed)
    print("AC:", ac)
    print("WA:", wa)
    print("Ans:", ans.strip()[:10])
    print()

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
    S = random.randint(MINS, MAXS)#max(MINS,int(2**(random.random()*log2(MAXS))))
    R = random.randint(MINR, min(S*(S-1)/2,MAXR))
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    #print(S,R)
    edges = random_edges(S, R)
    ps = smart_ps(S,M,C,edges,True)
    write_case("seed-%d" % seed, 5, S, R, M, C, ps, edges)

def test_sub2_seeds(n):
    global RUN_CASES
    RUN_CASES = False
    seed = 8581987
    wa = []
    for i in range(n):
        seed = (seed * 690006469) % 1000000007
        gen_sub2_seed(seed)
        copyfile("seed-%d-sub2.in" % seed, "stalls.in")
        ac = []
        wa = []
        for st in range(0,6):         
            os.system("sub%d < stalls.in > stalls.out" % st)
            os.system("grader > grader.out")
            if open("grader.out").read().startswith("AC"):
                ac.append(st)
            else:
                wa.append(st)
            if st == 2:
                ans = open("stalls.out").read()

        if 1:#len(wa) > 2:
            print(seed)
            print("AC:", ac)
            print("WA:", wa)
            print("Ans:", ans.strip())
            print()

def sub1():
    print("Generating subtask 1 cases...")
    random.seed(SEED)
    start_time = time.time()

    gen_complete("large-M=3", 1, 1413, 3, random.randint(0, int(1e9)))
    gen_complete("large-M=720", 1, 1414, 720, random.randint(0, int(1e9)))
    gen_complete("large-M=64000", 1, 1414, 64000, random.randint(0, int(1e9)))
    gen_complete("large-M=958711", 1, 1414, 958711, random.randint(0, int(1e9)))
    gen_complete("max", 1, 1414, 1000000000, random.randint(0, int(1e9)))

    S = 1414
    R = int((S*(S-1))/2)
    C = random.randint(2, int(1e7))
    M = 690006469
    ps = [463, 463]
    for i in range(S-2):
        ps.append(ne(ps[-1], M, C))

    # long chain work, begin at end
    write_case("chain-start", 1, S, R, M, C, ps, complete_edges(S))
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

    # C = 0
    C = 0
    ps = [0] + [random.randint(2, MAXP) for i in range(S-3)] + [1,1]
    random.shuffle(ps)
    write_case("C=0", 1, S, R, M, C, ps, complete_edges(S))

    print("--- %.6f seconds ---" % (time.time() - start_time))
    print()

def sub2():
    print("Generating subtask 2 cases...")
    start_time = time.time()

    #test_sub2_seeds(100)
    gen_sub2_seed(657163014) # WA: [] Ans: -1
    gen_sub2_seed(589697416) # WA: [] Ans: 0
    gen_sub2_seed(284964593) # WA: [] Ans: 1
    gen_sub2_seed(821887523) # WA: [3] Ans: -1
    gen_sub2_seed(53863356) # WA: [3, 4] Ans: -1
    gen_sub2_seed(229560240) # WA: [1] Ans: 1
    gen_sub2_seed(485620735) # WA: [1, 3] Ans: 2
    gen_sub2_seed(319189562) # WA: [1, 3, 4] Ans: 1
    gen_sub2_seed(347480376) # WA: [4] Ans: -1

    random.seed(SEED) # make sure each sub is the same, regardless of whether they are run individually or all together
    for i in range(6):
        S = 16
        R = random.randint(0, int(S*(S-1)/2))
        M = max(MINM,int(2**(random.random()*log2(MAXM))))
        C = max(MINC,int(2**(random.random()*log2(MAXC))))
        edges = random_edges(S, R)
        ps = smart_ps(S, M, C, edges, True)
        write_case("valid-%d" % (i + 1), 2, S, R, M, C, ps, edges)
    S = 16
    R = random.randint(0, int(S*(S-1)/2))
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = 0
    edges = random_edges(S, R)
    ps = smart_ps(S, M, C, edges, True)
    write_case("C=0", 2, S, R, M, C, ps, edges)

    print("--- %.6f seconds ---" % (time.time() - start_time))
    print()


def sub3():
    print("Generating subtask 3 cases...")
    random.seed(SEED)
    start_time = time.time()

    M = 3
    C = 2

    #odd cycle
    S = int(MAXS/2)*2 - 3
    R = S
    ps = random_ps(S, 1, 2)
    edges = cycle_edges(S)
    write_case("odd-cycle", 3, S, R, M, C, ps, edges)

    #even cycle
    S = int(MAXS/2)*2
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
    S = MAXS
    R = MAXR
    ps = random_ps(S, 1, 2)
    edges = bipartite_edges(S, R)
    write_case("random-bipartite", 3, S, R, M, C, ps, edges)
    """ 
    #random bipartite graph with all 2s
    S = 1000000
    R = 1000000
    ps = [2]*S
    edges = bipartite_edges(S, R)
    write_case("random-bipartite-all2s", 3, S, R, M, C, ps, edges)
    """
    #random non-bipartite
    S = MAXS
    R = MAXR
    ps = random_ps(S, 1, 2)
    edges = bipartite_edges(S, R-50000)
    make_non_bipartite(S, R, edges)
    write_case("random-non-bipartite", 3, S, R, M, C, ps, edges)

    #single edge non-bipartite
    S = MAXS
    R = MAXR
    ps = random_ps(S, 1, 2)
    edges = bipartite_edges(S, R-1)
    make_non_bipartite(S, R, edges)
    write_case("single-conflict-non-bipartite", 3, S, R, M, C, ps, edges)
    
    # random bipartite islands
    S = 0
    edges = []
    for i in range(1000):
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
    for i in range(1000):
        s = random.randint(1,180)
        r = random.randint(0, min(int(s*s/4), 200))
        merge_edges(edges, S, bipartite_edges(s, r), s)
        S += s
    merge_edges(edges, S, [(1, 2), (2, 3), (3, 1)], 3)
    S += 3
    R = len(edges)
    ps = random_ps(S, 1, 2)
    write_case("single-non-bipartite-island", 3, S, R, M, C, ps, edges)

    #tree
    S = MAXS
    R = S - 1
    edges = tree_to_edges(treegen.mixed_tree(S, 4))
    ps = random_ps(S, 1, 2)
    write_case("tree", 3, S, R, M, C, ps, edges)

    #no connections
    S = MAXS
    R = 0
    ps = random_ps(S, 1, 2)
    edges = []
    write_case("no-connections", 3, S, R, M, C, ps, edges)

    print("--- %.6f seconds ---" % (time.time() - start_time))
    print()

def sub4():
    print("Generating subtask 4 cases...")
    random.seed(SEED)
    start_time = time.time()

    # line broke
    S = MAXS
    R = S - 1
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    edges = line_edges(S)
    ps = smart_ps(S, M, C, edges)
    write_case("broke-line", 4, S, R, M, C, ps, edges)

    # line work
    S = MAXS
    R = S - 1
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    edges = line_edges(S)
    ps = smart_ps(S, M, C, edges, True)
    write_case("valid-line", 4, S, R, M, C, ps, edges)

    # random line
    S = MAXS
    R = S - 1
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    edges = line_edges(S)
    ps = random_ps(S)
    write_case("random-line", 4, S, R, M, C, ps, edges)

    # broke tree
    S = MAXS
    R = S - 1
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    edges = tree_to_edges(treegen.mixed_tree(S, 4))
    ps = smart_ps(S, M, C, edges)
    write_case("broke-tree", 4, S, R, M, C, ps, edges)

    # this took way too long to generate and has been included as a handmade case
    # valid tree
    S = 100000
    R = S - 1
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    edges = tree_to_edges(treegen.mixed_tree(S, 4))
    ps = smart_ps(S, M, C, edges, True)
    write_case("valid-tree", 4, S, R, M, C, ps, edges)

    # C=0
    S = 100000
    R = S - 1
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = 0
    edges = tree_to_edges(treegen.mixed_tree(S, 4))
    ps = smart_ps(S, M, C, edges, True)
    write_case("C=0-valid-tree", 4, S, R, M, C, ps, edges)


    #random tree
    S = MAXS
    R = S - 1
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    edges = tree_to_edges(treegen.mixed_tree(S, 4))
    ps = random_ps(S)
    write_case("random-tree", 4, S, R, M, C, ps, edges)

    print("--- %.6f seconds ---" % (time.time() - start_time))
    print()
 
def sub5():
    print("Generating subtask 5 cases...")
    random.seed(SEED)
    start_time = time.time()
    
    """
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
        copyfile("seed-%d-sub5.in" % seed, "stalls.in")
        #print("Testing %d..." % seed)
        ac = []
        wa = []
        for st in range(0,6):         
            os.system("sub%d < stalls.in > stalls.out" % st)
            os.system("grader > grader.out")
            if open("grader.out").read().startswith("AC"):
                ac.append(st)
            else:
                wa.append(st)
            if st == 5:
                ans = open("stalls.out").read()

        if 1:#len(wa) > 2:
            print(seed)
            print("AC:", ac)
            print("WA:", wa)
            print("Ans:", ans.strip()[:10])
            print()
    # 820497049
    """

    S = MAXS
    R = MAXR
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    edges = random_edges(S, R)
    ps = smart_ps(S, M, C, edges, True)
    write_case("max-valid", 5, S, R, M, C, ps, edges)

    S = MAXS
    R = MAXR
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    edges = random_edges(S, R)
    ps = smart_ps(S, M, C, edges)
    write_case("max-broke", 5, S, R, M, C, ps, edges)

    S = MAXS
    R = MAXR
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    edges = random_edges(S, R)
    ps = random_ps(S)
    write_case("max-random", 5, S, R, M, C, ps, edges)

    S = 100000
    R = MAXR
    M = MAXS
    C = 0
    edges = random_edges(S, R)
    ps = smart_ps(S, M, C, edges, True)
    write_case("max-C=0", 5, S, R, M, C, ps, edges)

    # valid islands
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    S = 0
    edges = []
    ps = []
    for i in range(1000):
        s = random.randint(1,180)
        r = random.randint(0, min(int(s*s/4), 200))
        es = random_edges(s, r)
        try:
            ps += smart_ps(s, M, C, es, True)
        except:
            continue
        merge_edges(edges, S, es, s)
        S += s
    R = len(edges)
    # ps = smart_ps(S, M, C, edges, True)
    write_case("valid-islands", 5, S, R, M, C, ps, edges)

    # 1 broke island
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    S = 0
    edges = []
    for i in range(1000):
        s = random.randint(1,180)
        r = random.randint(0, min(int(s*s/4), 200))
        merge_edges(edges, S, random_edges(s, r), s)
        S += s
    ps = smart_ps(S, M, C, edges, True)
    s = 200
    r = random.randint(0, int(s*s/4))
    broke_edges = random_edges(s, r)
    ps += smart_ps(s, M, C, broke_edges)
    merge_edges(edges, S, broke_edges, s)
    S += s
    R = len(edges)
    write_case("singl-broke-island", 5, S, R, M, C, ps, edges)

    #dense valid
    S = 5000
    R = MAXR
    M = 688137835
    C = 130
    edges = random_edges(S, R)
    ps = smart_ps(S, M, C, edges, True)
    write_case("dense-valid", 5, S, R, M, C, ps, edges)

    #dense broken
    S = 5000
    R = MAXR
    M = max(MINM,int(2**(random.random()*log2(MAXM))))
    C = max(MINC,int(2**(random.random()*log2(MAXC))))
    edges = random_edges(S, R)
    ps = smart_ps(S, M, C, edges)
    write_case("dense-broke", 5, S, R, M, C, ps, edges)

    print("--- %.6f seconds ---" % (time.time() - start_time))
    print()

# interactive interesting case
"""
M = 3
C = 2
S = 0
edges = []
for i in range(5):
    s = random.randint(1,30)
    r = random.randint(0, min(int(s*s/4), 200))
    merge_edges(edges, S, bipartite_edges(s, r), s)
    S += s
R = len(edges)
ps = random_ps(S, 1, 2)
write_case("bipartite-islands", 3, S, R, M, C, ps, edges)
"""

sub1()
sub2()
sub3()
sub4()
sub5()