from vm_translator import VMTranslator


def main():
    # root = sys.argv[1]
    root = "/Users/darlevy/PycharmProjects/vm-translator/StaticTest.vm"
    vm_translator = VMTranslator(root)
    vm_translator.translate()


if __name__ == '__main__':
    main()
