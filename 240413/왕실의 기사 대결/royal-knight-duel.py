from collections import deque
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def is_range(x, y):
    return 0<=x<L and 0<=y<L


def check_wall(r, c, h, w):
    for x, y in wall:
        if r<=x<=r+h-1 and c<=y<=c+w-1:
            return True
    return False


def check_trap(r, c, h, w):
    cnt = 0
    for x, y in trap:
        if r<=x<=r+h-1 and c<=y<=c+w-1:
           cnt += 1
    return cnt

def push(idx, direction):
    tmp = idx
    q = deque()
    is_moved= [False]*N
    is_moved[idx] = True
    q.append(idx)
    temp = [[] for _ in range(L)]
    while q:
        idx = q.popleft()
        r, c, h, w, k = knights[idx]
        if direction == 0:
            temp[idx] = [r-1, c, h, w, k]
            if not is_range(r - 1, c):
                return
            if check_wall(r-1, c, h, w):
                return
            for i in range(N):
                if is_moved[i]:
                    continue
                if not is_live[i]:
                    continue
                tr, tc, th, tw, tk = knights[i]
                if tr + th - 1 == r -1 and (c <= tc <= c+w-1 or c <= tc + tw-1 <= c+w-1):
                    q.append(i)
                    is_moved[i] = True

        elif direction == 1:
            temp[idx] = [r, c+1, h, w, k]
            if not is_range(r, c+1):
                return
            if check_wall(r, c+1, h, w):
                return
            for i in range(N):
                if is_moved[i]:
                    continue
                if not is_live[i]:
                    continue
                tr, tc, th, tw, tk = knights[i]
                if tc == c+w and (r <= tr <= r+h-1 or r <= tr+th-1 <= r+h-1):
                    q.append(i)
                    is_moved[i] = True

        elif direction == 2:
            temp[idx] = [r+1, c, h, w, k]
            if not is_range(r + 1, c):
                return
            if check_wall(r+1, c, h, w):
                return
            for i in range(N):
                if is_moved[i]:
                    continue
                if not is_live[i]:
                    continue
                tr, tc, th, tw, tk = knights[i]
                if tr == r + h and (c <= tc <= c+w-1 or c <= tc + tw-1 <= c+w-1):
                    q.append(i)
                    is_moved[i] = True

        elif direction == 3:
            temp[idx] = [r, c-1, h, w, k]
            if not is_range(r, c-1):
                return
            if check_wall(r, c-1, h, w):
                return
            for i in range(N):
                if is_moved[i]:
                    continue
                if not is_live[i]:
                    continue
                tr, tc, th, tw, tk = knights[i]
                if tc + tw-1 == c - 1 and (r <= tr <= r+h-1 or r <= tr+th-1 <= r+h-1):
                    q.append(i)
                    is_moved[i] = True

    for i in range(N):
        if is_moved[i]:
            knights[i] = temp[i]

    for i in range(N):
        if is_moved[i] and i != tmp:
            damage = check_trap(knights[i][0], knights[i][1], knights[i][2], knights[i][3])
            if damage >= knights[i][4]:
                is_live[i] = False
            else:
                knights[i][4] -= damage
                damaged[i] += damage

L, N, Q = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(L)]
wall = []
trap = []
damaged = [0] * N
for i in range(L):
    for j in range(L):
        if board[i][j] == 2:
            wall.append([i, j])
        elif board[i][j] == 1:
            trap.append([i, j])


knights = []
for _ in range(N):
    r, c, h, w, k = map(int, input().split())
    knights.append([r-1, c-1, h, w, k])
orders = [list(map(int, input().split())) for _ in range(Q)]
is_live = [True for _ in range(N)]



for idx, direction in orders:
    push(idx-1, direction)

ans = 0
for i in range(N):
    if is_live[i]:
        ans += damaged[i]
print(ans)