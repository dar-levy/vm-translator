import sys

from vm_translator import VMTranslator


def main():
    vm_translator = VMTranslator(sys.argv[1])
    vm_translator.translate()


if __name__ == '__main__':
    main()
