# Ray Tracer in a Weekend (in Python)
# Chapter 1 - Output an image

if __name__ == '__main__':
    nx = 200
    ny = 100

    print(f'P3\n{nx} {ny}\n255')
    for j in range(ny, 0, -1):
        for i in range(nx):
            r = float(i) / float(nx)
            g = float(j) / float(ny)
            b = 0.2
            ir = int(255.99 * r)
            ig = int(255.99 * g)
            ib = int(255.99 * b)
            print(f'{ir} {ig} {ib}')
