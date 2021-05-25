import sys
import getopt


def get_cml_arg(argv) -> str:
    inputfile = ''
    outputfile = ''
    try:
        # opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        #Input arguments without mentioned
        # print('test.py -i <inputfile> -o <outputfile>')
        print('> Do not have this argument. Only support "-tv" or "-m"')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':     #help
            print('test.py -tv <inputfile> -m <outputfile>')
            sys.exit()
        elif opt in ("-tv", "-tvshow", "-tvshows"):
            inputfile = arg
        elif opt in ("-m", "-movie", "-movies"):
            outputfile = arg
    print('Input file is "', inputfile)
    print('Output file is "', outputfile)


def main(argv):
    get_cml_arg(argv)


if __name__ == "__main__":
    main(sys.argv[1:])


