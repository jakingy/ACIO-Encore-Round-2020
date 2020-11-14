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
def point_based_ranges(H, n = 1):
    pts = [random.random()for _ in range(n)]
    ranges = []
    while len(ranges) < 2**H-2:
        ai = random.random()
        bi = random.random()
        ai,bi = min(ai,bi),max(ai,bi)
        for pt in pts:
            if ai <= pt and pt <= bi:
                ranges.append((ai,bi))
                break
    return ranges

def rep_random(lo, hi, n):
    ret = 1
    for i in range(n):
        ret *= random.random() * (hi-lo) + lo
    return ret

# the upper ranges are usually bigger
def top_biased_ranges(H, off_bias):
    ranges = []
    nranges = 2**H-2
    sz_sort = []
    for i in range(nranges):
        bi = random.random()
        sz_sort.append((bi * rep_random(1 - off_bias, 1 + off_bias, 2),bi))
    sz_sort.sort()
    sz_sort.reverse()
    szs = [sz[1] for sz in sz_sort]  
    for i in range(nranges):
        sz = szs[i]
        ai = random.random() * (1-sz)
        bi = ai + sz
        ranges.append((ai,bi))
    return ranges

def patitioning_ranges(H):
    ranges = [(),(0,1)]
    for i in range(2,2**H):
        par = i//2
        if i%2:
            ranges.append((ranges[i-1][1],ranges[par][1]))
        else:
            split = random.random() * (ranges[par][1]-ranges[par][0]) + ranges[par][0]
            ranges.append((ranges[par][0],split))
    return ranges[2:]
        
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

def query_root(H, Q):
    N = 2**H-1
    qs = []
    for i in range(Q):
        R = random.random()
        qs.append((1,R))
    return qs

def sub2_queries(H, Q):
    qs = []
    for i in range(Q):
        X = random.randrange(2**(H-2), 2**(H-1))
        R = random.random()
        qs.append((X,R))
    return qs

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
    print("Generating", fname)
    with open(fname + '.in', "w") as case_file:
        case_file.write("%d\n" % H)
        for r in ranges:
            case_file.write("%f %f\n" % r)
        case_file.write("%d\n" % Q)
        random.shuffle(qs)
        for q in qs:
            case_file.write("%d %f\n" % q)

Q = 100000

#tiny
H = 2
ranges = random_ranges(H)
qs = sub2_queries(H, Q)
write_case("tiny2-sub2", H, Q, ranges, qs)

H = 2
ranges = random_ranges(H, 0.05, 0.06)
qs = sub2_queries(H, Q)
write_case("tiny2-small-ranges-sub2", H, Q, ranges, qs)

H = 3
ranges = random_ranges(H)
qs = sub2_queries(H, Q)
write_case("tiny3-sub2", H, Q, ranges, qs)

H = 3
ranges = random_ranges(H, 0.999, 1.0)
qs = sub2_queries(H, Q)
write_case("tiny3-small-ranges-sub2", H, Q, ranges, qs)

#small
H = random.choice(H_SMALL)
ranges = random_ranges(H, random.random() * .5, random.random() * .5 + .5)
qs = sub2_queries(H, Q)
write_case("small-random-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = no_overlapping_ranges(H)
qs = sub2_queries(H, Q)
write_case("small-no-overlapping-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = point_based_ranges(H)
qs = sub2_queries(H, Q)
write_case("small-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = point_based_ranges(H, 2)
qs = sub2_queries(H, Q)
write_case("small-2-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = point_based_ranges(H, 4)
qs = sub2_queries(H, Q)
write_case("small-4-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = top_biased_ranges(H, 0.08)
qs = sub2_queries(H, Q)
write_case("small-top-biased-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = top_biased_ranges(H, 0.3)
qs = sub2_queries(H, Q)
write_case("small-top-biased-ranges2-sub2", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = top_biased_ranges(H, 0.7)
qs = sub2_queries(H, Q)
write_case("small-top-biased-ranges3-sub2", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = patitioning_ranges(H)
qs = sub2_queries(H, Q)
write_case("small-patitioning-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = patitioning_ranges(H)
qs = sub2_queries(H, Q)
write_case("small-patitioning-ranges-sub2", H, Q, ranges, qs)

#med
H = random.choice(H_MED)
ranges = random_ranges(H, random.random() * .5, random.random() * .5 + .5)
qs = sub2_queries(H, Q)
write_case("med-random-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = no_overlapping_ranges(H)
qs = sub2_queries(H, Q)
write_case("med-no-overlapping-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = point_based_ranges(H)
qs = sub2_queries(H, Q)
write_case("med-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = point_based_ranges(H, 2)
qs = sub2_queries(H, Q)
write_case("med-2-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = point_based_ranges(H, 4)
qs = sub2_queries(H, Q)
write_case("med-4-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = top_biased_ranges(H, 0.08)
qs = sub2_queries(H, Q)
write_case("med-top-biased-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = top_biased_ranges(H, 0.3)
qs = sub2_queries(H, Q)
write_case("med-top-biased-ranges2-sub2", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = top_biased_ranges(H, 0.7)
qs = sub2_queries(H, Q)
write_case("med-top-biased-ranges3-sub2", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = patitioning_ranges(H)
qs = sub2_queries(H, Q)
write_case("med-patitioning-ranges-sub2", H, Q, ranges, qs)

#large
H = random.choice(H_LARGE)
ranges = random_ranges(H, random.random() * .5, random.random() * .5 + .5)
qs = sub2_queries(H, Q)
write_case("large-random-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = no_overlapping_ranges(H)
qs = sub2_queries(H, Q)
write_case("large-no-overlapping-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H)
qs = sub2_queries(H, Q)
write_case("large-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H)
qs = sub2_queries(H, Q)
write_case("large-point-based-ranges2-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 2)
qs = sub2_queries(H, Q)
write_case("large-2-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 2)
qs = sub2_queries(H, Q)
write_case("large-2-point-based-ranges2-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 4)
qs = sub2_queries(H, Q)
write_case("large-4-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 8)
qs = sub2_queries(H, Q)
write_case("large-8-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 16)
qs = sub2_queries(H, Q)
write_case("large-16-point-based-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.05)
qs = sub2_queries(H, Q)
write_case("large-top-biased-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.2)
qs = sub2_queries(H, Q)
write_case("large-top-biased-ranges2-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.4)
qs = sub2_queries(H, Q)
write_case("large-top-biased-ranges3-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.75)
qs = sub2_queries(H, Q)
write_case("large-top-biased-ranges4-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.99)
qs = sub2_queries(H, Q)
write_case("large-top-biased-ranges5-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = patitioning_ranges(H)
qs = sub2_queries(H, Q)
write_case("large-patitioning-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0, 0.5)
qs = sub2_queries(H, Q)
write_case("large-random-sized-ranges-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.5, 1)
qs = sub2_queries(H, Q)
write_case("large-random-sized-ranges2-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.9, 1)
qs = sub2_queries(H, Q)
write_case("large-random-sized-ranges3-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.99, 1)
qs = sub2_queries(H, Q)
write_case("large-random-sized-ranges4-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.45, 0.7)
qs = sub2_queries(H, Q)
write_case("large-random-sized-ranges5-sub2", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0, 0.1)
qs = sub2_queries(H, Q)
write_case("large-random-sized-ranges6-sub2", H, Q, ranges, qs)
