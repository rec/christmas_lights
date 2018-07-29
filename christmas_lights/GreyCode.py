def gray_code(count):
    def recurse(g, n):
        if n <= 0:
            return

        r = range(len(g) - 1, -1, -1)
        for i in r:
            char = '1' + g[i]
            g.append(char)

        for i in r:
            g[i] = '0' + g[i]

        recurse(g, n - 1)

    g = ['0', '1']
    recurse(g, count - 1)
    return g


if __name__ == '__main__':
    print(gray_code(3))
