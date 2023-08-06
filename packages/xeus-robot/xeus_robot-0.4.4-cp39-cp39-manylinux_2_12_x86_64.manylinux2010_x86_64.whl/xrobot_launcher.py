if __name__ == '__main__':
    import sys
    from xrobot import launch as _xrobot_launch
    args_list = sys.argv[:]
    sys.argv = sys.argv[:1]  # Remove unnecessary arguments
    _xrobot_launch(args_list)
