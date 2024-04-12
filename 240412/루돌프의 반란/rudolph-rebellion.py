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
    closetidx, closetx, closety = 0, 100000, 100000

    for i in range(1, P + 1):
        if not is_alive[i]:
            continue

        currentBest = ((closestX - rudolf[0]) ** 2 + (closestY - rudolf[1]) ** 2, (-closestX, -closestY))
        currentValue = ((pos[i][0] - rudolf[0]) ** 2 + (pos[i][1] - rudolf[1]) ** 2, (-pos[i][0], -pos[i][1]))

        if currentValue < currentBest:
            closestX, closestY = pos[i]
            closestIdx = i

        # 가장 가까운 산타의 방향으로 루돌프가 이동합니다.
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

        # 루돌프의 이동으로 충돌한 경우, 산타를 이동시키고 처리를 합니다.
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
    for i in range(1, P + 1):
        if not is_alive[i] or stun[i] >= t:
            continue

        minDist = (pos[i][0] - rudolf[0]) ** 2 + (pos[i][1] - rudolf[1]) ** 2
        moveDir = -1

        for dir in range(4):
            nx = pos[i][0] + dx[dir]
            ny = pos[i][1] + dy[dir]

            if not is_inrange(nx, ny) or board[nx][ny] > 0:
                continue

            dist = (nx - rudolf[0]) ** 2 + (ny - rudolf[1]) ** 2
            if dist < minDist:
                minDist = dist
                moveDir = dir

        if moveDir != -1:
            nx = pos[i][0] + dx[moveDir]
            ny = pos[i][1] + dy[moveDir]

            # 산타의 이동으로 충돌한 경우, 산타를 이동시키고 처리를 합니다.
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
                    # 만약 이동한 위치에 산타가 있을 경우, 연쇄적으로 이동이 일어납니다.
                    while is_inrange(lastX, lastY) and board[lastX][lastY] > 0:
                        lastX += moveX
                        lastY += moveY

                    # 연쇄적으로 충돌이 일어난 가장 마지막 위치에서 시작해,
                    # 순차적으로 보드판에 있는 산타를 한칸씩 이동시킵니다.
                    while lastX != firstX or lastY != firstY:
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

                    points[i] += D
                    board[pos[i][0]][pos[i][1]] = 0
                    pos[i] = (firstX, firstY)
                    if is_inrange(firstX, firstY):
                        board[firstX][firstY] = i
                    else:
                        is_alive[i] = 0
            else:
                board[pos[i][0]][pos[i][1]] = 0
                pos[i] = (nx, ny)
                board[nx][ny] = i

    for i in range(1, P+1):
        if is_alive[i]:
            points[i] += 1




for i in range(1, P+1):
    print(points[i], end=" ")