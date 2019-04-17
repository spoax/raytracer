# Ray Tracer in a Weekend (in Python)
# Chapter 1 - Output an image in a window


def make_color(r0, g0, b0):
    return '#{0:02x}{1:02x}{2:02x}'.format(r0, g0, b0)


def save_image(img, format):
    import os
    img.write(os.path.basename(__file__).split('.')[0] + '.' + format, format=format)


if __name__ == '__main__':
    nx = 200
    ny = 100

    from tkinter import *

    main = Tk()
    w = Canvas(main, width=nx, height=ny)
    w.pack()

    img = PhotoImage(width=nx, height=ny)

    for j in range(ny):
        for i in range(nx):
            r = float(i) / float(nx)
            g = float(j) / float(ny)
            b = 0.2
            ir = int(255.99 * r)
            ig = int(255.99 * g)
            ib = int(255.99 * b)
            c = make_color(ir, ig, ib)
            img.put(c, (i, ny-j))

    w.create_image((nx/2, ny/2), image=img, state="normal")

    save_image(img, 'ppm')

    mainloop()
