def is_range(r, c):
    return 1<=r<=N and 1<=c<=N

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

N,M,P,C,D = map(int, input().split())
rudolf = list(map(int, input().split()))

board = [[0 for _ in range(N+1)] for _ in range(N+1)]
is_live = [True for _ in range(P+1)]
pos = [[0, 0] for _ in range(P+1)]
stun = [0 for _ in range(P+1)]
points = [0 for _ in range(P+1)]


for _ in range(P):
    idx, r, c = map(int, input().split())
    pos[idx] = [r, c]
    board[r][c] = idx

board[rudolf[0]][rudolf[1]] = -1

for t in range(1, M+1):
    closestX, closestY, closestIdx = 10000, 10000, 0

    for i in range(1, P+1):
        if not is_live[i]:
            continue
        minDist = (rudolf[0] - closestX)**2 + (rudolf[1] - closestY)**2
        tempDist = (rudolf[0] - pos[i][0])**2 + (rudolf[1] - pos[i][1])**2

        if tempDist < minDist:
            closestX, closestY = pos[i]
            closestIdx = i
        elif tempDist == minDist:
            if pos[i][0] > closestX:
                closestX, closestY = pos[i]
                closestIdx = i
            elif pos[i][0] == closestX and pos[i][1] > closestY:
                closestX, closestY = pos[i]
                closestIdx = i
    if closestIdx:
        prevX, prevY = rudolf
        moveX, moveY = 0, 0
        if closestX > prevX:
            moveX = 1
        elif closestX < prevX:
            moveX = -1

        if closestY > prevY:
            moveY = 1
        elif closestY < prevY:
            moveY = -1
        rudolf = [prevX + moveX, prevY + moveY]
        board[prevX][prevY] = 0
    if rudolf[0] == closestX and rudolf[1] == closestY:
        prevX, prevY = closestX, closestY
        nextX, nextY = closestX + moveX * C, closestY + moveY * C
        prevIdx = board[prevX][prevY]
        points[closestIdx] += C
        stun[closestIdx] = t + 1
        while True:
            if not is_range(nextX, nextY):
                is_live[board[prevX][prevY]] = False
                break

            if not board[nextX][nextY] > 0:
                pos[prevIdx] = [nextX, nextY]
                board[nextX][nextY] = prevIdx
                break

            tempIdx = board[nextX][nextY]
            board[nextX][nextY] = prevIdx
            pos[prevIdx] = [nextX, nextY]

            prevX, prevY = nextX, nextY
            nextX, nextY = prevX+moveX, prevY+moveY
            prevIdx = tempIdx
    board[rudolf[0]][rudolf[1]] = -1


    for i in range(1, P+1):
        if not is_live[i] or stun[i] >= t:
            continue

        minDist = (pos[i][0] - rudolf[0])**2 + (pos[i][1] - rudolf[1])**2
        moveDir = -1

        for k in range(4):
            nx = pos[i][0] + dx[k]
            ny = pos[i][1] + dy[k]
            if not is_range(nx, ny):
                continue

            if board[nx][ny] > 0:
                continue

            dist = (nx - rudolf[0])**2 + (ny - rudolf[1])**2

            if dist < minDist:
                moveDir = k
                minDist = dist

        if moveDir == -1:
             continue

        nx = pos[i][0] + dx[moveDir]
        ny = pos[i][1] + dy[moveDir]
        if nx == rudolf[0] and ny == rudolf[1]:
            stun[i] = t + 1
            prevX, prevY = pos[i][0], pos[i][1]
            nextX, nextY = nx - dx[moveDir]*D, ny - dy[moveDir]*D
            prevIdx = board[prevX][prevY]
            if D == 1:
                points[i] += D
            else:
                while True:
                    if not is_range(nextX, nextY):
                        is_live[prevIdx] = False
                        break

                    if not board[nextX][nextY] > 0:
                        board[nextX][nextY] = prevIdx
                        pos[prevIdx] = [nextX, nextY]
                        break

                    tempIdx = board[nextX][nextY]
                    board[nextX][nextY] = prevIdx
                    pos[prevIdx] = [nextX, nextY]

                    prevX, prevY = nextX, nextY
                    prevIdx = tempIdx
                    nextX, nextY = prevX - dx[moveDir], prevY - dy[moveDir]

                points[i] += D
                board[nx - dx[moveDir]][ny - dy[moveDir]] = 0
        else:
            board[pos[i][0]][pos[i][1]] = 0
            board[nx][ny] = i
            pos[i] = [nx, ny]

    for i in range(1, P+1):
        if is_live[i]:
            points[i] += 1


for i in range(1, P+1):
    print(points[i], end=" ")