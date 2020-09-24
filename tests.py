from main import next_board_state, render

if __name__ == '__main__':
    #Rule 1
    init_state = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]

    expected_state = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    actual_next = next_board_state(init_state)

    if expected_state == actual_next:
        print('Passed 1\n')
    else:
        print('Failed 1')
        print('Expected:\n{}'.format(render(expected_state)))
        print('Actual:\n{}'.format(render(actual_next)))
        print('--------\n')

    #Rule 2
    init_state = [
        [0,0,1],
        [0,1,1],
        [0,0,0]
    ]

    expected_state = [
        [0,1,1],
        [0,1,1],
        [0,0,0]
    ]
    actual_next = next_board_state(init_state)

    if expected_state == actual_next:
        print('Passed 2\n')
    else:
        print('Failed 2')
        print('Expected:\n{}'.format(render(expected_state)))
        print('Actual:\n{}'.format(render(actual_next)))
        print('--------\n')

    #Rule 3 & 4
    init_state = [
        [0,1,0],
        [1,1,1],
        [0,1,0]
    ]

    expected_state = [
        [1,1,1],
        [1,0,1],
        [1,1,1]
    ]
    actual_next = next_board_state(init_state)

    if expected_state == actual_next:
        print('Passed 3\n')
    else:
        print('Failed 3')
        print('Expected:\n{}'.format(render(expected_state)))
        print('Actual:\n{}'.format(render(actual_next)))
        print('--------\n')
