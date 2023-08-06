import logging
import sys
from sh import tail
import importlib.util


def main():
    if len(sys.argv) < 2:
        print('Missing argument log path')
        sys.exit(1)
    if len(sys.argv) < 3:
        print('Missing argument module path')
        sys.exit(1)
    log_path = sys.argv[1]
    module_path = sys.argv[2]
    spec = importlib.util.spec_from_file_location("module.name", module_path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    for line in tail("-f", log_path, _iter=True):
        try:
            foo.process_line(line)
        except Exception as ex:
            logging.error(ex)


if __name__ == '__main__':
    main()
