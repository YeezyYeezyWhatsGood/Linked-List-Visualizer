import pygame
from collections import deque
# constants
display_width, display_height = 800, 600
radius = 30  # node size


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def linked_list(linked_list_values, cycle_location):
    if not linked_list_values:
        return None
    head = ListNode(linked_list_values[0])
    curr = head
    cycle_node = head
    for i, val in enumerate(linked_list_values[1:], 1):
        new_node = ListNode(val)
        curr.next = new_node
        curr = new_node
        if i == cycle_location:
            cycle_node = new_node
    curr.next = None if cycle_location == -1 else cycle_node
    return head


def make_graph(linked_list_values, cycle_location):
    graph = []
    sep = 3 * radius
    for i, val in enumerate(linked_list_values, 1):
        graph.append(((i * sep, sep), val))
    if cycle_location == -1:
        graph.append((((len(linked_list_values) + 1) * sep, sep), "None"))
    return graph


def floyd(head):
    q = deque()
    if head is None:
        return q
    slow = head
    fast = head.next
    while slow != fast:
        q.append((slow, fast))
        if fast is None:
            return q
        if fast.next is None:
            q.append((slow.next, fast.next))
            return q
        slow = slow.next
        fast = fast.next.next
    q.append((slow, fast))
    return q

def brent(head):
    # https://en.wikipedia.org/wiki/Cycle_detection#Brent's_algorithm
    q = deque()
    if head is None:
        return q
    power = lam = 1
    tortoise = head
    hare = head.next
    while tortoise != hare:
        q.append((tortoise, hare))
        if hare is None:
            return q
        if power == lam:
            tortoise = hare
            power *= 2
            lam = 0
        hare = hare.next
        lam += 1
    q.append((tortoise, hare))
    return q


def run_floyd(linked_list_values, cycle_location):
    graph = make_graph(linked_list_values, cycle_location)
    pygame.init()
    head = linked_list(linked_list_values, cycle_location)
    q = floyd(head)
    node_to_index = {}
    curr = head
    for i in range(len(linked_list_values)):
        node_to_index[curr] = i
        curr = curr.next
    screen = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    camxy = [-3 * radius, 0]
    speed = 6
    slow, fast = 0, 0
    if q:
        tempslow, tempfast = q.popleft()
        slow, fast = node_to_index[tempslow], node_to_index[
            tempfast] if tempfast else len(linked_list_values)
    auto = False
    auto_slow = False
    just_pressed_s = False
    just_pressed_f = False
    delay = 750
    while 1:
        clock.tick(45)
        if auto:
            if not just_pressed_f:
                pygame.time.wait(delay)
            just_pressed_f = False
            if q:
                tempslow, tempfast = q.popleft()
                slow = node_to_index[tempslow]
                fast = node_to_index[tempfast] if tempfast else len(
                    linked_list_values)
                camxy[0] = (fast - 2) * 3 * radius
            else:
                auto = False

        if auto_slow:
            if not just_pressed_s:
                pygame.time.wait(delay)
            just_pressed_s = False
            if q:
                tempslow, tempfast = q.popleft()
                slow = node_to_index[tempslow]
                fast = node_to_index[tempfast] if tempfast else len(
                    linked_list_values)
                camxy[0] = (slow - 2) * 3 * radius
            else:
                auto_slow = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            camxy[0] -= speed
        if keys[pygame.K_RIGHT]:
            camxy[0] += speed
        if keys[pygame.K_UP]:
            camxy[1] -= speed
        if keys[pygame.K_DOWN]:
            camxy[1] += speed

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not auto:
                    if q:
                        tempslow, tempfast = q.popleft()
                        slow = node_to_index[tempslow]
                        fast = node_to_index[tempfast] if tempfast else len(
                            linked_list_values)
                if event.key == pygame.K_a:
                    camxy[0] = -3*radius
                if event.key == pygame.K_d:
                    camxy[0] = (len(linked_list_values) - 1) * 3 * radius
                if event.key == pygame.K_c:
                    if cycle_location != -1:
                        camxy[0] = cycle_location * 3 * radius
                if event.key == pygame.K_f:
                    auto_slow = False
                    just_pressed_f = True
                    if auto:
                        auto = False
                    elif q:
                        camxy = [-3 * radius, 0]
                        auto = True
                if event.key == pygame.K_s:
                    auto = False
                    just_pressed_s = True
                    if auto_slow:
                        auto_slow = False
                    elif q:
                        camxy = [-3 * radius, 0]
                        auto_slow = True
                if event.key == pygame.K_r:
                    q = floyd(head)
                    slow, fast = 0, 0
                    if q:
                        tempslow, tempfast = q.popleft()
                        slow, fast = node_to_index[tempslow], node_to_index[
                            tempfast] if tempfast else len(linked_list_values)
                if event.key == pygame.K_1:
                    speed = 4
                    delay = 2250
                if event.key == pygame.K_2:
                    speed = 6
                    delay = 750
                if event.key == pygame.K_3:
                    speed = 8
                    delay = 250

        screen.fill((0, 0, 0))  # param is color tuple

        img_slow = font.render("slow", True, (255, 0, 0))
        img_fast = font.render("fast", True, (0, 255, 0))
        loc_slow = (graph[slow][0][0] - camxy[0] - radius +
                    (2 * radius - img_slow.get_size()[0]) / 2,
                    graph[slow][0][1] - 2 * radius - camxy[1])
        loc_fast = (graph[fast][0][0] - camxy[0] - radius +
                    (2 * radius - img_fast.get_size()[0]) / 2,
                    graph[fast][0][1] + radius - camxy[1])

        screen.blit(img_slow, loc_slow)
        screen.blit(img_fast, loc_fast)

        # loop to draw cicle at each node center
        for centerxy, val in graph[:-1]:
            loc = (centerxy[0] - camxy[0], centerxy[1] - camxy[1])
            start = (loc[0] + radius, loc[1])
            end = (loc[0] + radius * 2, loc[1])
            pygame.draw.circle(
                screen,  # draw need buffer
                (255, 255, 200),  # color of circle
                loc,
                radius)  # default is filled circle
            pygame.draw.circle(screen, (0, 150, 150), loc, radius - 5)
            pygame.draw.line(screen, (255, 255, 255), start, end)
            pygame.draw.line(screen, (255, 255, 255),
                             end, (end[0] - radius / 4, end[1] + radius / 4),
                             width=2)
            pygame.draw.line(screen, (255, 255, 255),
                             end, (end[0] - radius / 4, end[1] - radius / 4),
                             width=2)
            img = font.render(str(val), True, (0, 0, 0))
            screen.blit(img, (loc[0] - img.get_size()[0] / 2,
                              loc[1] - img.get_size()[1] / 2))

        loc = (graph[-1][0][0] - camxy[0], graph[-1][0][1] - camxy[1])
        start = (loc[0] + radius, loc[1])
        end = (loc[0] + radius * 2, loc[1])
        pygame.draw.circle(
            screen,  # draw need buffer
            (255, 255, 200),  # color of circle
            loc,
            radius)  # default is filled circle
        pygame.draw.circle(screen, (0, 150, 150), loc, radius - 5)
        img = font.render(str(graph[-1][1]), True, (0, 0, 0))
        screen.blit(
            img,
            (loc[0] - img.get_size()[0] / 2, loc[1] - img.get_size()[1] / 2))
        if cycle_location != -1:
            pygame.draw.line(screen, (255, 255, 255),
                             (loc[0] + radius, loc[1]),
                             (loc[0] + radius, loc[1] + 2 * radius))
            pygame.draw.line(
                screen, (255, 255, 255),
                (loc[0] + radius, loc[1] + 2 * radius),
                (graph[cycle_location][0][0] - camxy[0], loc[1] + 2 * radius))
            pygame.draw.line(
                screen, (255, 255, 255),
                (graph[cycle_location][0][0] - camxy[0], loc[1] + 2 * radius),
                (graph[cycle_location][0][0] - camxy[0], loc[1] + radius))
            pygame.draw.line(
                screen, (255, 255, 255),
                (graph[cycle_location][0][0] - camxy[0], loc[1] + radius),
                (graph[cycle_location][0][0] - camxy[0] - radius / 4,
                 loc[1] + radius + radius / 4),
                width=2)
            pygame.draw.line(
                screen, (255, 255, 255),
                (graph[cycle_location][0][0] - camxy[0], loc[1] + radius),
                (graph[cycle_location][0][0] - camxy[0] + radius / 4,
                 loc[1] + radius + radius / 4),
                width=2)


        pygame.display.update()  # copy screen to display

def run_brent(linked_list_values, cycle_location):
    graph = make_graph(linked_list_values, cycle_location)
    pygame.init()
    head = linked_list(linked_list_values, cycle_location)
    q = brent(head)
    node_to_index = {}
    curr = head
    for i in range(len(linked_list_values)):
        node_to_index[curr] = i
        curr = curr.next
    screen = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    camxy = [-3 * radius, 0]
    speed = 6
    slow, fast = 0, 0
    if q:
        tempslow, tempfast = q.popleft()
        slow, fast = node_to_index[tempslow], node_to_index[
            tempfast] if tempfast else len(linked_list_values)
    auto = False
    auto_slow = False
    just_pressed_s = False
    just_pressed_f = False
    delay = 750
    while 1:
        clock.tick(45)
        if auto:
            if not just_pressed_f:
                pygame.time.wait(delay)
            just_pressed_f = False
            if q:
                tempslow, tempfast = q.popleft()
                slow = node_to_index[tempslow]
                fast = node_to_index[tempfast] if tempfast else len(
                    linked_list_values)
                camxy[0] = (fast - 2) * 3 * radius
            else:
                auto = False

        if auto_slow:
            if not just_pressed_s:
                pygame.time.wait(delay)
            just_pressed_s = False
            if q:
                tempslow, tempfast = q.popleft()
                slow = node_to_index[tempslow]
                fast = node_to_index[tempfast] if tempfast else len(
                    linked_list_values)
                camxy[0] = (slow - 2) * 3 * radius
            else:
                auto_slow = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            camxy[0] -= speed
        if keys[pygame.K_RIGHT]:
            camxy[0] += speed
        if keys[pygame.K_UP]:
            camxy[1] -= speed
        if keys[pygame.K_DOWN]:
            camxy[1] += speed

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not auto:
                    if q:
                        tempslow, tempfast = q.popleft()
                        slow = node_to_index[tempslow]
                        fast = node_to_index[tempfast] if tempfast else len(
                            linked_list_values)
                if event.key == pygame.K_a:
                    camxy[0] = -3*radius
                if event.key == pygame.K_d:
                    camxy[0] = (len(linked_list_values) - 1) * 3 * radius
                if event.key == pygame.K_c:
                    if cycle_location != -1:
                        camxy[0] = cycle_location * 3 * radius
                if event.key == pygame.K_f:
                    auto_slow = False
                    just_pressed_f = True
                    if auto:
                        auto = False
                    elif q:
                        camxy = [-3 * radius, 0]
                        auto = True
                if event.key == pygame.K_s:
                    auto = False
                    just_pressed_s = True
                    if auto_slow:
                        auto_slow = False
                    elif q:
                        camxy = [-3 * radius, 0]
                        auto_slow = True
                if event.key == pygame.K_r:
                    q = brent(head)
                    slow, fast = 0, 0
                    if q:
                        tempslow, tempfast = q.popleft()
                        slow, fast = node_to_index[tempslow], node_to_index[
                            tempfast] if tempfast else len(linked_list_values)
                if event.key == pygame.K_1:
                    speed = 4
                    delay = 2250
                if event.key == pygame.K_2:
                    speed = 6
                    delay = 750
                if event.key == pygame.K_3:
                    speed = 8
                    delay = 250

        screen.fill((0, 0, 0))  # param is color tuple

        img_slow = font.render("tortoise", True, (255, 0, 0))
        img_fast = font.render("hare", True, (0, 255, 0))
        loc_slow = (graph[slow][0][0] - camxy[0] - radius +
                    (2 * radius - img_slow.get_size()[0]) / 2,
                    graph[slow][0][1] - 2 * radius - camxy[1])
        loc_fast = (graph[fast][0][0] - camxy[0] - radius +
                    (2 * radius - img_fast.get_size()[0]) / 2,
                    graph[fast][0][1] + radius - camxy[1])

        screen.blit(img_slow, loc_slow)
        screen.blit(img_fast, loc_fast)

        # loop to draw cicle at each node center
        for centerxy, val in graph[:-1]:
            loc = (centerxy[0] - camxy[0], centerxy[1] - camxy[1])
            start = (loc[0] + radius, loc[1])
            end = (loc[0] + radius * 2, loc[1])
            pygame.draw.circle(
                screen,  # draw need buffer
                (255, 255, 200),  # color of circle
                loc,
                radius)  # default is filled circle
            pygame.draw.circle(screen, (0, 150, 150), loc, radius - 5)
            pygame.draw.line(screen, (255, 255, 255), start, end)
            pygame.draw.line(screen, (255, 255, 255),
                             end, (end[0] - radius / 4, end[1] + radius / 4),
                             width=2)
            pygame.draw.line(screen, (255, 255, 255),
                             end, (end[0] - radius / 4, end[1] - radius / 4),
                             width=2)
            img = font.render(str(val), True, (0, 0, 0))
            screen.blit(img, (loc[0] - img.get_size()[0] / 2,
                              loc[1] - img.get_size()[1] / 2))

        loc = (graph[-1][0][0] - camxy[0], graph[-1][0][1] - camxy[1])
        start = (loc[0] + radius, loc[1])
        end = (loc[0] + radius * 2, loc[1])
        pygame.draw.circle(
            screen,  # draw need buffer
            (255, 255, 200),  # color of circle
            loc,
            radius)  # default is filled circle
        pygame.draw.circle(screen, (0, 150, 150), loc, radius - 5)
        img = font.render(str(graph[-1][1]), True, (0, 0, 0))
        screen.blit(
            img,
            (loc[0] - img.get_size()[0] / 2, loc[1] - img.get_size()[1] / 2))
        if cycle_location != -1:
            pygame.draw.line(screen, (255, 255, 255),
                             (loc[0] + radius, loc[1]),
                             (loc[0] + radius, loc[1] + 2 * radius))
            pygame.draw.line(
                screen, (255, 255, 255),
                (loc[0] + radius, loc[1] + 2 * radius),
                (graph[cycle_location][0][0] - camxy[0], loc[1] + 2 * radius))
            pygame.draw.line(
                screen, (255, 255, 255),
                (graph[cycle_location][0][0] - camxy[0], loc[1] + 2 * radius),
                (graph[cycle_location][0][0] - camxy[0], loc[1] + radius))
            pygame.draw.line(
                screen, (255, 255, 255),
                (graph[cycle_location][0][0] - camxy[0], loc[1] + radius),
                (graph[cycle_location][0][0] - camxy[0] - radius / 4,
                 loc[1] + radius + radius / 4),
                width=2)
            pygame.draw.line(
                screen, (255, 255, 255),
                (graph[cycle_location][0][0] - camxy[0], loc[1] + radius),
                (graph[cycle_location][0][0] - camxy[0] + radius / 4,
                 loc[1] + radius + radius / 4),
                width=2)


        pygame.display.update()  # copy screen to display
