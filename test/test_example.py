def test_equal_or_not_equal():
    num_list = [1, 2, 3, 4, 5]
    false_list = [False, False]
    true_list = [True, True]

    assert 1 in num_list
    assert 8 not in num_list
    assert all(num_list)
    assert not all(false_list)
    assert all(false_list)
    assert all(true_list)
    assert not all(true_list)
    assert not any(false_list)