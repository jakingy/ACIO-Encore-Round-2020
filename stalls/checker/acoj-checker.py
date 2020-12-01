from dmoj.result import CheckerResult
from dmoj.utils.unicode import utf8bytes


def check(process_output: bytes, judge_output: bytes, judge_input: bytes, **kwargs) -> bool:
    def ne(x):
        return (x * C) % M;
    try:
        input_ints = list(map(int,utf8bytes(judge_input).decode().split()))
        correct_output = list(map(int,utf8bytes(judge_output).decode().split()))
        contestant_output = list(map(int,utf8bytes(process_output).decode().split()))
        S,R,M,C = input_ints[:4]
        p = [0] + [input_ints[4+i] % M for i in range(S)]
        adj = [[] for i in range(S+1)]
        for i in range(R):
            a,b = input_ints[4+S+i*2:6+S+i*2]
        x = correct_output[0]
        n = contestant_output[0]
        if x == -1:
            if n != -1:
                return False
        else:
            stalls = contestant_output[1:]
            if n != len(stalls): #The council's powers were not used the indicated number of times.
                return False
            if len(set(stalls)) != n: #Used the council's power more than once on the same stall.
                return False
            for stall in stalls:
                if stall < 1 or stall > S: #Stall number outside range [1, S]
                    return False
                p[stall] = ne(p[stall])
            for u in range(1,S+1):
                for v in adj[u]:
                    if p[u] == p[v]: #Stall list is not valid
                        return False     
        return True
    except:
        return False
