def check_brackets(string, pairs = {'[': ']', '{': '}', '(': ')'}):

    opening = list(pairs.keys())

    closing = list(pairs.values())

    match = list()

    for s in string:
        if s in opening:
            match.insert(0, s)
        elif s in closing:
            if len(match) == 0:
                return False
            if match[0] == opening[closing.index(s)]:
                match.pop(0)
            else:
                return False

    if len(match) == 0:
        return True

    return False

if __name__ == "__main__":
    import time

    millis = float(time.time() * 1000)

    string = "[]{}()[][][]"
    print("Should be true")
    print(str(check_brackets(str(string))))

    string = "([()][][{}])"
    print("Should be true")
    print(str(check_brackets(string)))

    string = "[(])"
    print("Should be false")
    print(str(check_brackets(string)))

    string = "[([])()({})]"
    print("Should be true")
    print(str(check_brackets(string)))

    string = "[(,,),(,,[])]"
    print("Should be true")
    print(str(check_brackets(string)))

    string = "[(,,,(,,[])]"
    print("Should be false")
    print(str(check_brackets(string)))

    string = "]"
    print("Should be false")
    print(str(check_brackets(string)))

    string = "["
    print("Should be false")
    print(str(check_brackets(string)))

    string = "{[{}][][({})]}"
    print("Should be true")
    print(str(check_brackets(string)))

    string = """
        public static void main(String args[])
        {
            System.out.println("Hello world");
        }
    """

    print("Should be true")
    print(str(check_brackets(string)))

    string = "[[[((({{{}}})))]]]"
    print("Should be true")
    print(str(check_brackets(string)))

    millis = float(time.time() * 1000) - millis
    print("Result " + str(millis))