import random
random.seed(238769756)

MAXN = 1000

def relative_proportions(N, M, rP, rT, rE):
    total = float(rP + rT + rE)
    P = int(N*M * rP / total)
    T = int(N*M * rT / total)
    if T == N*M:
        T -= 1
    return P,T

def gen_random(N, M, P, T):
    grid = [['.']*M for _ in range(N)]
    points = [(n,m) for m in range(M) for n in range(N)][:-1]
    random.shuffle(points)
    for i in range(T):
        r,c = points.pop()
        grid[r][c] = 'T'

    points.append((N-1,M-1))
    random.shuffle(points)

    for i in range(P):
        r,c = points.pop()
        grid[r][c] = 'P'

    return grid

def gen_maxcase(N, M):
    grid = [['P']*M for _ in range(N)]
    if M > 1: grid[-1][-2] = 'T'
    if N > 1: grid[-2][-1] = 'T'
    return grid

def validate_grid(grid):
    N = len(grid)
    M = len(grid[0])
    
    if N < 1:
        raise Exception("N < 1")
    if M < 1:
        raise Exception("M < 1")
    if N > MAXN:
        raise Exception("N > %d" % MAXN)
    if M > MAXN:
        raise Exception("M > %d" % MAXN)
    if grid[-1][-1] == 'T':
        raise Exception("bottom-right square is a T") 

    if any(len(row) != M for row in grid):
        raise Exception("M changed")

def write_case(name, grid):
    print("Generating", name)
    N = len(grid)
    M = len(grid[0])
    validate_grid(grid)
    with open(name + '.in', 'w') as case_file:
        case_file.write("%d %d\n" % (N,M))
        case_file.write('\n'.join(''.join(row) for row in grid) + '\n')

grid = [['P']]
write_case('min', grid)

#sub 1
for i in range(5):
    N = random.randint(1,MAXN)
    M = random.randint(1,MAXN)
    P,T = relative_proportions(N,M,random.random(),0,random.random())
    grid = gen_random(N,M,P,T)
    write_case('random-%d-sub1' % i, grid)

N = M = MAXN

P,T = relative_proportions(N,M,0,0,1)
grid = gen_random(N,M,P,T)
write_case('large-empty-sub1', grid)

P,T = relative_proportions(N,M,1,0,10000)
grid = gen_random(N,M,P,T)
write_case('large-very-sparse-sub1', grid)

P,T = relative_proportions(N,M,1,0,100)
grid = gen_random(N,M,P,T)
write_case('large-sparse-sub1', grid)

P,T = relative_proportions(N,M,1,0,1)
grid = gen_random(N,M,P,T)
write_case('large-even-sub1', grid)

P,T = relative_proportions(N,M,100,0,1)
grid = gen_random(N,M,P,T)
write_case('large-dense-sub1', grid)

P,T = relative_proportions(N,M,100,0,0)
grid = gen_random(N,M,P,T)
write_case('max-sub1', grid)

# sub 2
for i in range(5):
    N = 1
    M = random.randint(1,MAXN)
    P = random.randrange(0, M-1)
    T = 1
    grid = gen_random(N,M,P,T)
    write_case('random-%d-sub2' % i, grid)

N = 1
M = MAXN
T = 1

P = 0
grid = gen_random(N,M,P,T)
write_case('large-empty-sub2', grid)

P = 1
grid = gen_random(N,M,P,T)
write_case('large-single-sub2', grid)

P = 3
grid = gen_random(N,M,P,T)
write_case('large-very-sparse-sub2', grid)

P = 23
grid = gen_random(N,M,P,T)
write_case('large-sparse-sub2', grid)

P = 500
grid = gen_random(N,M,P,T)
write_case('large-even-sub2', grid)

P = 900
grid = gen_random(N,M,P,T)
write_case('large-dense-sub2', grid)

P = 999
grid = gen_random(N,M,P,T)
write_case('large-full-sub2', grid)

grid = gen_maxcase(1,MAXN)
write_case('max-sub2', grid)

# sub 3
for i in range(7):
    N = random.randint(1,MAXN)
    M = random.randint(1,MAXN)
    P,T = relative_proportions(N,M,random.random(),random.random(),random.random())
    grid = gen_random(N,M,P,T)
    write_case('random-%d-sub3' % i, grid)



density = [0, 0.01, 1, 100, 10000000000]
dnames = ["empty", "sparse", "even", "dense", "full"]
for dP in range(len(density)):
    for dT in range(len(density)):
        N = random.randint(1,MAXN)
        N = random.randint(1,MAXN)
        P,T = relative_proportions(N,M,density[dP],density[dT],1)
        grid = gen_random(N,M,P,T)
        write_case('%s-potatoes-%s-teleporters-sub3' % (dnames[dP], dnames[dT]), grid)

grid = gen_maxcase(MAXN,1)
write_case('skinny-sub3', grid)

grid = gen_random(MAXN, MAXN, 0, MAXN * MAXN - 1)
grid[-1][-1] = 'P'
write_case('teleporters-corner-potato-sub3', grid)

grid = gen_maxcase(MAXN,MAXN)
write_case('max-sub3', grid)



