import random
random.seed(19877529)

MAXH = 17
MAXQ = 100000

def no_overlapping_ranges(H):
    rng = sorted([random.random()for i in range(2**(H+1)-4)])
    return [(rng[i],rng[i+1]) for i in range(0,len(rng),2)]

def random_ranges(H, lo = 0, hi = 1):
    ranges = []
    for i in range(2**H-2):
        ai = random.random() * (hi-lo) + lo
        bi = random.random() * (hi-lo) + lo
        ai,bi = min(ai,bi),max(ai,bi)
        ranges.append((ai,bi))
    return ranges

def random_sized_ranges(H, lo = 0, hi = 1):
    ranges = []
    for i in range(2**H-2):
        sz = random.random() * (hi-lo) + lo
        ai = random.random() * (1-sz)
        bi = ai + sz
        ranges.append((ai,bi))
    return ranges
 
# generate n random points, each range must contain at least one point.
def maxcase_ranges(H):
    ranges = [(random.random(),1) for i in range(2**H-2)]
    return ranges

def sub3_maxcase_ranges(H):
    ranges = [(0,1) for i in range(2**H-2)]
    return ranges
        
def random_queries(H, Q):
    N = 2**H-1
    qs = []
    for i in range(Q):
        X = random.randint(1, N)
        R = random.random()
        qs.append((X,R))
    return qs

def stratified_queries(H, Q):
    qs = []
    for i in range(Q):
        d = random.randint(0, H-1)
        X = random.randrange(2**d, 2**(d+1))
        R = random.random()
        qs.append((X,R))
    return qs

def query_all_at_point(H, Q, pt):
    qs = []
    for i in range(Q):
        qs.append(((i-1)%(2**H-1)+1, pt))
    return qs

def maxcase_queries(H, Q):
    return query_all_at_point(H, 70000, 1) + stratified_queries(H, 30000)


# small, medium and large of each of the following:
# random bis random queries
# random bis stratified queries
# top biased bis random queries
# top biased bis stratified queries
# top biased bis med stratified queries
# top biased bis lesser stratified queries
# sub3 already catered for fully sorted bis

H_SMALL = list(range(4, 7))
H_MED = list(range(9, 13))
H_LARGE = [17]#list(range(15, 18))

def write_case(fname, H, Q, ranges, qs):
    with open(fname + '.in', "w") as case_file:
        case_file.write("%d\n" % H)
        for r in ranges:
            case_file.write("%f %f\n" % r)
        case_file.write("%d\n" % Q)
        random.shuffle(qs)
        for q in qs:
            case_file.write("%d %f\n" % q)

Q = 100000
H = 17

ranges = maxcase_ranges(H)
qs = maxcase_queries(H, Q)
write_case("max-sub5", H, Q, ranges, qs)

ranges = sub3_maxcase_ranges(H)
qs = maxcase_queries(H, Q)
write_case("max-sub3", H, Q, ranges, qs)

ranges = maxcase_ranges(H)
qs = query_all_at_point(H, Q, 1)
write_case("max-sub1", H, Q, ranges, qs)