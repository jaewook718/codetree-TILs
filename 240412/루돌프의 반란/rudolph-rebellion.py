dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
N, M, P, C, D = map(int, input().split())
rudolf = list(map(int, input().split()))

board = [[0 for _ in range(N+1)] for _ in range(N+1)]
pos = [[0, 0] for _ in range(P+1)]
is_alive = [1 for _ in range(P+1)]
stun = [0 for _ in range(P+1)]
points = [0 for _ in range(P+1)]

for _ in range(P):
    id, x, y = map(int, input().split())
    pos[id] = [x, y]
    board[x][y] = id

board[rudolf[0]][rudolf[1]] = -1


for t in range(1, M+1):
    closetidx, closetx, closety = 0, 100000, 100000

    for i in range(1, P+1):
        if is_alive[i] == 1:
            closetdist = (rudolf[0] - closetx)**2 + (rudolf[1] - closety)**2
            currentdist = (rudolf[0] - pos[i][0])**2 + (rudolf[1] - pos[i][1])**2
            if currentdist < closetdist:
                closetidx = i
                closetx, closety = pos[closetidx]
            elif currentdist == closetdist:
                if closetx < pos[i][0]:
                    closetidx = i
                    closetx, closety = pos[closetidx]
                elif closetx == pos[i][0]:
                    if closety < pos[i][1]:
                        closetidx = i
                        closetx, closety = pos[closetidx]

    if closetidx:
        prevRudolf = rudolf
        moveX, moveY = 0, 0
        if closetx > rudolf[0]:
            moveX = 1
        elif closetx < rudolf[0]:
            moveX = -1
        if closety > rudolf[1]:
            moveY = 1
        elif closety < rudolf[1]:
            moveY = -1
        rudolf = [rudolf[0] + moveX, rudolf[1] + moveY]
        board[prevRudolf[0]][prevRudolf[1]] = 0

        if rudolf[0] == closetx and rudolf[1] == closety:
            firstX = closetx + moveX * C
            firstY = closety + moveY * C
            lastX, lastY = firstX, firstY
            stun[closetidx] = t+1

            while 1<=lastX<=N and 1<=lastY<=N and board[lastX][lastY]:
                lastX += moveX
                lastY += moveY

            while not(lastX == firstX and lastY == firstY):
                beforeX = lastX - moveX
                beforeY = lastY - moveY
                if not (1<=beforeX<=N and 1<=beforeY<=N):
                    break

                idx = board[beforeX][beforeY]

                if not (1<=lastX<N and 1<=lastY<=N):
                    is_alive[idx] = 0
                else:
                    board[lastX][lastY] = idx
                    pos[idx] = [lastX, lastY]

                lastX, lastY = beforeX, beforeY

            points[closetidx] += C
            pos[closetidx] = [firstX, firstY]
            if 1<=firstX<=N and 1<=firstY<=N:
                board[firstX][firstY] = closetidx
            else:
                is_alive[closetidx] = 0

        board[rudolf[0]][rudolf[1]] = -1
    for i in range(1, P+1):
        if is_alive[i] == 0 or stun[i] >= t:
            continue
        dist = (pos[i][0] - rudolf[0])**2 + (pos[i][1] - rudolf[1])**2
        moveDir = -1
        for k in range(4):
            nx = pos[i][0] + dx[k]
            ny = pos[i][1] + dy[k]

            if not (1<=nx<=N and 1<=ny<=N) or board[nx][ny] > 0:
                continue

            tempdist = (nx - rudolf[0])**2 + (ny - rudolf[1])**2
            if dist > tempdist:
                moveDir = k
                dist = tempdist
        if moveDir == -1:
            continue

        nx = pos[i][0] + dx[moveDir]
        ny = pos[i][1] + dy[moveDir]
        if nx == rudolf[0] and ny == rudolf[1]:
            stun[i] = t + 1

            moveX = -dx[moveDir]
            moveY = -dy[moveDir]

            firstX = nx + moveX * D
            firstY = ny + moveY * D
            lastX, lastY = firstX, firstY
            if D == 1:
                points[i] += D
            else:
                while 1<=lastX<=N and 1<=lastY<=N and board[lastX][lastY] > 0:
                    lastX += moveX
                    lastY += moveY
                while lastX != firstY or lastY != firstY:

                    beforeX = lastX - moveX
                    beforeY = lastY - moveY
                    if not (1<=beforeX<=N and 1<=beforeY<=N):
                        break

                    idx = board[beforeX][beforeY]

                    if not (1<=lastX<=N and 1<=lastY<=N):
                        is_alive[idx] = 0
                    else:
                        board[lastX][lastY] = board[beforeX][beforeY]
                        pos[idx] = [lastX, lastY]

                    lastX, lastY = beforeX, beforeY
                points[i] += D
                board[pos[i][0]][pos[i][1]] = 0
                pos[i] = [firstX, firstY]
                if 1<=firstX<=N and 1<=firstY<=N:
                    board[firstX][firstY] = i
                else:
                    is_alive[i] = 0

        else:
            board[pos[i][0]][pos[i][1]] = 0
            pos[i] = [nx, ny]
            board[nx][ny] = i

    for i in range(1, P+1):
        if is_alive[i]:
            points[i] += 1




for i in range(1, P+1):
    print(points[i], end=" ")