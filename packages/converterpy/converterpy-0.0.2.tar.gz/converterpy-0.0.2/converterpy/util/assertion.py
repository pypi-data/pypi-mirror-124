def assert_list_is_instance(iterable, expected_type):
    for i in iterable:
        assert isinstance(i, expected_type)


def assert_with_thrown(fn, exception_class, assertion_fn, assertion_message=None):
    raised = False
    try:
        fn()
    except exception_class as e:
        if assertion_fn(e):
            raised = True
    finally:
        assert raised, assertion_message
