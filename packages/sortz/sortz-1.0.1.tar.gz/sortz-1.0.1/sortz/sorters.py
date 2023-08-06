def bubble_sort(bars):
    """
    A simple bubble sort generator that sorts a single value
    of the array per iteration.

    Parameters
    ----------
    bars : List[Tuple[pygame.Surface, pygame.Rect]]
        A list of game objects to be sorted by height

    Returns
    -------
    is_sorted : bool
        Has the array been sorted?
    """

    unsorted_until_index = len(bars) - 1
    is_sorted = False

    while not is_sorted:
        is_sorted = True

        for i in range(unsorted_until_index):
            if bars[i][1].height > bars[i + 1][1].height:
                bars[i], bars[i + 1] = bars[i + 1], bars[i]
                is_sorted = False
                yield is_sorted

        unsorted_until_index -= 1

    yield is_sorted
