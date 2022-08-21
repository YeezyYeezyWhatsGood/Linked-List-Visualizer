import pygame
# constants
display_width, display_height = 800, 600
radius = 30  # node size


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def linked_list(linked_list_values, cycle_location):
    # given a list of values and the location of a cycle (if no cycle this is -1) generates a linked list
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
    # given a list of values and the location of a cycle (if no cycle this is -1)
    # returns a list with entries of the form ((x_coor, y_coor), val)
    graph = []
    sep = 3 * radius  # the diameter of a node is 2 * radius and each node is seperated by a distance of radius
    for i, val in enumerate(linked_list_values, 1):
        graph.append(((i * sep, sep), val))
    if cycle_location == -1:
        graph.append((((len(linked_list_values) + 1) * sep, sep), "None"))
    return graph


def floyd(head):
    # https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare
    q = []
    if head is None:
        return q
    slow = head
    fast = head.next
    while slow != fast:
        q.append((slow, fast))
        if fast is None or fast.next is None:
            return q
        slow = slow.next
        fast = fast.next.next
    q.append((slow, fast))
    return q


def brent(head):
    # https://en.wikipedia.org/wiki/Cycle_detection#Brent's_algorithm
    q = []
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


def run(linked_list_values, cycle_location, algorithm):
    graph = make_graph(linked_list_values, cycle_location)  # make the graph
    pygame.init()  # start the game
    head = linked_list(linked_list_values,
                       cycle_location)  # create the linked list
    pointer_arr = algorithm(
        head
    )  # run the algorithm of choice on the linked list (returns an array of tuples corresponding to the location of the fast and slow pointers at any given step of the algorithm)
    algo_stage = 0  # passed as an index to pointer_arr, tells us what step of the algorithm we are at
    node_to_index = {
    }  # make a dictionary where the keys are nodes of the linked list and the values are the index of that node in linked_list_values (this allows us to locate it in our visualization)
    curr = head
    for i in range(len(linked_list_values)):
        node_to_index[curr] = i
        curr = curr.next
    screen = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    camxy = [-3 * radius, 0]  # x and y coordinates of where our camera is
    speed = 6  # speed for when you move with the arrow keys
    auto_fast = False  # whether or not you are automatically following the fast pointer
    auto_slow = False  # whether or not you are automatically following the slow pointer
    just_pressed_s = False  # if you just pressed s (to follow the slow pointer) skip the delay
    just_pressed_f = False  # if you just pressed s (to follow the slow pointer) skip the delay
    delay = 750  # when automatically following the slow or fast pointer how many milliseconds to wait before going to the next step of the algorithm
    while 1:  # game loop
        clock.tick(45)  # 45 fps

        # calculate which indexes of linked_list_values slow and fast are on
        # note that if fast is on None then we have no cycle and want None to be the last node of the linked list
        # ie for input linked_list_values = [1, 2,3, 4] cycle_location = -1 we get 1->2->3->4->None so None's "index" is 4 = len(linked_list_values)
        tempslow, tempfast = pointer_arr[algo_stage]
        slow = node_to_index[tempslow]
        fast = node_to_index[tempfast] if tempfast else len(linked_list_values)

        if auto_fast:  # if we are following the fast pointer
            if not just_pressed_f:  # wait a delay unless you just pressed f (to start following the pointer)
                pygame.time.wait(delay)
            just_pressed_f = False
            if algo_stage != len(
                    pointer_arr
            ) - 1:  # if the algorithm hasn't finished running
                # go to the next step of the algorithm and move the camera to the fast pointer
                algo_stage += 1
                camxy[0] = (fast - 2) * 3 * radius
                camxy[1] = 0
            else:  # if the algorithm is finished stop following fast
                auto_fast = False

        if auto_slow:  # same as above but for following the slow pointer instead
            if not just_pressed_s:
                pygame.time.wait(delay)
            just_pressed_s = False
            if algo_stage != len(pointer_arr) - 1:
                algo_stage += 1
                camxy[0] = (slow - 2) * 3 * radius
                camxy[1] = 0
            else:
                auto_slow = False

        keys = pygame.key.get_pressed(
        )  # see what keys are currently being pressed

        # move the camera with the arrow keys
        if keys[pygame.K_LEFT]:
            camxy[0] -= speed
        if keys[pygame.K_RIGHT]:
            camxy[0] += speed
        if keys[pygame.K_UP]:
            camxy[1] -= speed
        if keys[pygame.K_DOWN]:
            camxy[1] += speed

        # an event is triggered when something "new" happens
        # ie if you hold down the left key although keys[pygame.K_LEFT] will be true every frame it is held down
        # but an event for pressing down the left key will only be triggered once
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:  # if a key was pushed down
                # if you press enter go to the next stage of the algorithm
                # unless of course you are following the slow or fast pointer or the algorithm is finshed running
                if event.key == pygame.K_RETURN and not (auto_fast
                                                         or auto_slow):
                    if algo_stage != len(pointer_arr) - 1:
                        algo_stage += 1

                # press a to send the camera to the beginning of the linked list
                if event.key == pygame.K_a:
                    camxy[0] = -3 * radius
                    camxy[1] = 0
                # press d to send the camera to the end of the linked list
                if event.key == pygame.K_d:
                    camxy[0] = (len(linked_list_values) - 1) * 3 * radius
                    camxy[1] = 0
                # press c to send the camera to where the cycle happens
                if event.key == pygame.K_c:
                    if cycle_location != -1:  # of course only do this if there is a cycle
                        camxy[
                            0] = cycle_location * 3 * radius  # each circle is 2 radius big and seperated from the previous circle by a distance of radius
                        camxy[1] = 0
                # press f to toggle automatically following the fast pointer
                if event.key == pygame.K_f:
                    auto_slow = False  # stop automatically following the slow pointer
                    just_pressed_f = True  # we just pressed f (this lets us skip the first delay)
                    if auto_fast:  # if we were already following the fast pointer then stop
                        auto_fast = False
                    elif algo_stage != len(
                            pointer_arr
                    ) - 1:  # if we weren't following the fast pointer already and our algo isnt done
                        camxy = [-3 * radius, 0]
                        auto_fast = True
                # press s to toggle automatically following the slow pointer
                if event.key == pygame.K_s:
                    auto_fast = False  # stop automatically following the fast pointer
                    just_pressed_s = True  # we just pressed s (this lets us skip the first delay)
                    if auto_slow:  # if we were already following the slow pointer then stop
                        auto_slow = False
                    elif algo_stage != len(
                            pointer_arr
                    ) - 1:  # if we weren't following the slow pointer already and our algo isnt done
                        camxy = [-3 * radius, 0]
                        auto_slow = True
                # press r to reset the algorithm back to step one
                if event.key == pygame.K_r:
                    algo_stage = 0  # back to step one of the algorithm
                    camxy = [-3 * radius,
                             0]  # reset our camera too for convenience
                # press 1 to go to slow speed
                if event.key == pygame.K_1:
                    speed = 4  # speed of arrow keys
                    delay = 2250  # delay from step to step when you're automatically following fast or slow
                # press 2 to go to medium speed
                if event.key == pygame.K_2:
                    speed = 6
                    delay = 750
                # press 3 to go to fast speed
                if event.key == pygame.K_3:
                    speed = 8
                    delay = 250
                # press backspace to go back a step (but don't do this if you're at the first step or are following fast or slow)
                if event.key == pygame.K_BACKSPACE and not (auto_fast
                                                            or auto_slow):
                    if algo_stage != 0:
                        algo_stage -= 1

        screen.fill((0, 0, 0))  # set the background to black
        # used different names for the pointers in the different algorithms
        if algorithm == floyd:
            # in the floyd algorithm we call the slow and fast pointers slow and fast
            slow_text = "slow"
            fast_text = "fast"
        if algorithm == brent:
            # in the brent algorithm we call the slow and fast algorithm tortise and hare like in Aesop's fable
            slow_text = "tortoise"
            fast_text = "hare"
        img_slow = font.render(
            slow_text, True,
            (255, 0, 0))  # render the slow text as a red image
        img_fast = font.render(
            fast_text, True,
            (0, 255, 0))  # render the fast text as a green image
        # calculate the xy coordinates of the slow and fast pointers. this is a bit confusing so let me explain
        # graph[slow] is of the form ((x_coord, y_coor), value), so we acess the x and y coord of slow as graph[slow][0][0] and graph[slow][0][1]
        # for the x coordinate we then subtract radius to shift it to the left and subtract camxy[0] make it relative to our camera position and add half the difference between the diameter and the width of the text to center it
        # for the y coordinate we subtract the radius twice to move it on top of the circle and then substract the y coordinate of our camera to make it relative to our camera position
        # fast works simialrly
        loc_slow = (graph[slow][0][0] - camxy[0] - radius +
                    (2 * radius - img_slow.get_size()[0]) / 2,
                    graph[slow][0][1] - 2 * radius - camxy[1])
        loc_fast = (graph[fast][0][0] - camxy[0] - radius +
                    (2 * radius - img_fast.get_size()[0]) / 2,
                    graph[fast][0][1] + radius - camxy[1])

        # add the text for the fast and slow pointers onto the screen
        screen.blit(img_slow, loc_slow)
        screen.blit(img_fast, loc_fast)

        # draw each node except for the last one
        for centerxy, val in graph[:-1]:
            loc = (centerxy[0] - camxy[0], centerxy[1] - camxy[1]
                   )  # adjust the location of our node to the camera position
            start = (
                loc[0] + radius, loc[1]
            )  # where the line connecting this node to the next node will start
            end = (
                loc[0] + radius * 2, loc[1]
            )  # where the line connecting this node to the next node will end
            # draw our pretty nodes by drawing a circle inside another circle
            pygame.draw.circle(
                screen,  # draw need buffer
                (255, 255, 200),  # color of circle
                loc,
                radius)  # default is filled circle
            pygame.draw.circle(screen, (0, 150, 150), loc, radius - 5)
            # draw the arrow connecting this node to the next node (note (255, 255, 255) represents the color white)
            pygame.draw.line(screen, (255, 255, 255), start,
                             end)  # line from this node to the next
            pygame.draw.line(screen, (255, 255, 255),
                             end, (end[0] - radius / 4, end[1] + radius / 4),
                             width=2)  # first part of the "arrow tip"
            pygame.draw.line(screen, (255, 255, 255),
                             end, (end[0] - radius / 4, end[1] - radius / 4),
                             width=2)  # second part of the "arrow tip"
            # put the value of the node inside the circle
            img = font.render(str(val), True, (0, 0, 0))
            screen.blit(
                img,
                (loc[0] - img.get_size()[0] / 2, loc[1] - img.get_size()[1] /
                 2))  # subtract half the size of the image to center it

        # loc, start, end as before but for the last node
        loc = (graph[-1][0][0] - camxy[0], graph[-1][0][1] - camxy[1])
        start = (loc[0] + radius, loc[1])
        end = (loc[0] + radius * 2, loc[1])
        # draw the node as before but for the last node
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
        # if there is a cycle then draw and arrow from the last node to where the cycle is
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
