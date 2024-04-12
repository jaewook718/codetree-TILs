def is_inrange(x, y):
    return 1 <= x and x <= N and 1 <= y and y <= N
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
    closestX, closestY, closestIdx = 10000, 10000, 0

    # 살아있는 포인트 중 루돌프에 가장 가까운 산타를 찾습니다.
    for i in range(1, P + 1):
        if is_alive[i] == 1:
            closetdist = (rudolf[0] - closestX) ** 2 + (rudolf[1] - closestY) ** 2
            currentdist = (rudolf[0] - pos[i][0]) ** 2 + (rudolf[1] - pos[i][1]) ** 2
            if currentdist < closetdist:
                closestIdx = i
                closestX, closestY = pos[closestIdx]
            elif currentdist == closetdist:
                if closestX < pos[i][0]:
                    closestIdx = i
                    closestX, closestY = pos[closestIdx]
                elif closestX == pos[i][0]:
                    if closestY < pos[i][1]:
                        closestIdx = i
                        closestX, closestY = pos[closestIdx]

    if closestIdx:
        prevRudolf = rudolf
        moveX = 0
        if closestX > rudolf[0]:
            moveX = 1
        elif closestX < rudolf[0]:
            moveX = -1

        moveY = 0
        if closestY > rudolf[1]:
            moveY = 1
        elif closestY < rudolf[1]:
            moveY = -1

        rudolf = (rudolf[0] + moveX, rudolf[1] + moveY)
        board[prevRudolf[0]][prevRudolf[1]] = 0

    if rudolf[0] == closestX and rudolf[1] == closestY:
        firstX = closestX + moveX * C
        firstY = closestY + moveY * C
        lastX, lastY = firstX, firstY

        stun[closestIdx] = t + 1

        # 만약 이동한 위치에 산타가 있을 경우, 연쇄적으로 이동이 일어납니다.
        while is_inrange(lastX, lastY) and board[lastX][lastY] > 0:
            lastX += moveX
            lastY += moveY

        # 연쇄적으로 충돌이 일어난 가장 마지막 위치에서 시작해,
        # 순차적으로 보드판에 있는 산타를 한칸씩 이동시킵니다.
        while not (lastX == firstX and lastY == firstY):
            beforeX = lastX - moveX
            beforeY = lastY - moveY

            if not is_inrange(beforeX, beforeY):
                break

            idx = board[beforeX][beforeY]

            if not is_inrange(lastX, lastY):
                is_alive[idx] = 0
            else:
                board[lastX][lastY] = board[beforeX][beforeY]
                pos[idx] = (lastX, lastY)

            lastX, lastY = beforeX, beforeY

        points[closestIdx] += C
        pos[closestIdx] = (firstX, firstY)
        if is_inrange(firstX, firstY):
            board[firstX][firstY] = closestIdx
        else:
            is_alive[closestIdx] = 0

    board[rudolf[0]][rudolf[1]] = -1;
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

            tempdist = (nx - rudolf[0])**2 + (ny -rudolf[1])**2
            if dist > tempdist:
                moveDir = k
                dist = tempdist
        if moveDir == -1:
            continue

        nx = pos[i][0] + dx[moveDir]
        ny = pos[i][1] + dy[moveDir]
        if nx == rudolf[0] and ny == rudolf[1]:
            stun[i] = t + 1

            firstX = nx - dx[moveDir] * D
            firstY = ny - dy[moveDir] * D
            lastX, lastY = firstX, firstY
            if D == 1:
                points[i] += 1
            else:
                while 1<=lastX<=N and 1<=lastY<=N and board[lastX][lastY] > 0:
                    lastX -= dx[moveDir]
                    lastY -= dy[moveDir]
                while not (lastX==firstX and lastY==firstY):

                    beforeX = lastX + dx[moveDir]
                    beforeY = lastY + dy[moveDir]
                    if not (1<=beforeX<=N and 1<=beforeY<=N):
                        break

                    idx = board[beforeX][beforeY]

                    if not (1<=lastX<=N and 1<=lastY<=N):
                        is_alive[idx] = 0
                    else:
                        board[lastX][lastY] = idx
                        pos[idx] = [lastX, lastY]

                    lastX, lastY = beforeX, beforeY
                if 1<=firstX<=N and 1<=firstY<=N:
                    board[firstX][firstY] = i
                else:
                    is_alive[i] = 0
                points[i] += D
                board[pos[i][0]][pos[i][1]] = 0
                pos[i] = [firstX, firstY]
        else:
            board[pos[i][0]][pos[i][1]] = 0
            pos[i] = [nx, ny]
            board[nx][ny] = i

    for i in range(1, P+1):
        if is_alive[i]:
            points[i] += 1




for i in range(1, P+1):
    print(points[i], end=" ")