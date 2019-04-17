# Ray Tracer in a Weekend (in Python)
# Chapter 9 - Dielectrics

import math

from random import random


class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def r(self): return self.x

    @property
    def g(self): return self.y

    @property
    def b(self): return self.z

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vec3(self.x / other, self.y / other, self.z / other)

    def __rmul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def cross(a, b):
        return Vec3( (a.y * b.z - a.z * b.y),
                    -(a.x * b.z - a.z * b.x),
                     (a.x * b.y - a.y * b.x))

    @staticmethod
    def length(a):
        return math.sqrt(Vec3.dot(a, a))

    @staticmethod
    def squared_length(a):
        return Vec3.dot(a, a)

    @staticmethod
    def unit_vector(v):
        return v / Vec3.length(v)


class Ray:
   def __init__(self, origin, direction):
       """
       :param origin: origin vector of the ray
       :param direction: direction vector of the ray
       :type origin: Vec3
       :type direction: Vec3
       """
       self.origin = origin
       self.direction = direction

   def point_at(self, t):
       return self.origin + self.direction * t


class HitRecord:
    def __init__(self, t = None, p = None, normal = None):
        """
        :type t: float
        :type p: Vec3
        :type normal: Vec3
        """
        self.t = t
        self.p = p
        self.normal = normal
        self.material = None


class Hitable:
    def hit(self, r, t_min, t_max):
        """
        :type r: Ray
        :type t_min: float
        :type t_max: float
        :rtype: HitRecord
        """
        raise NotImplementedError()


class Material:
    def scatter(self, r_in, rec):
        """

        :type r_in: Ray
        :type rec: HitRecord
        :rtype: tuple(Boolean, Ray scattered, Vec3 attenuation)
        """
        raise NotImplementedError()


class HitableList(Hitable):
    def __init__(self, l):
        self.list = l

    def hit(self, r, t_min, t_max):
        closest_so_far = t_max
        rec = None
        for h in self.list:
            temp_rec = h.hit(r, t_min, closest_so_far)
            if temp_rec is not None:
                closest_so_far = temp_rec.t
                rec = temp_rec
        return rec


class Sphere(Hitable):
    def __init__(self, center, radius, material):
        """
        :type center: Vec3
        :type radius: float
        """
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r, t_min, t_max):
        oc = r.origin - self.center
        a = Vec3.dot(r.direction, r.direction)
        b = Vec3.dot(oc, r.direction)
        c = Vec3.dot(oc, oc) - self.radius * self.radius
        discriminant = b*b - a*c
        if discriminant > 0.0:
            rec = HitRecord()
            temp = (-b - math.sqrt(discriminant)) / a
            if t_min < temp < t_max:
                rec.t = temp
                rec.p = r.point_at(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                rec.material = self.material
                return rec

            temp = (-b + math.sqrt(discriminant)) / a
            if t_min < temp < t_max:
                rec.t = temp
                rec.p = r.point_at(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                rec.material = self.material
                return rec

        return None


class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec):
        target = rec.p + rec.normal + random_in_unit_sphere()
        scattered = Ray(rec.p, target - rec.p)
        attenuation = self.albedo
        return True, scattered, attenuation


def reflect(v, n):
    """
    :type v: Vec3
    :type n: Vec3
    :return: Reflected ray
    """
    return v - 2 * Vec3.dot(v, n) * n


def refract(v, n, ni_over_nt):
    """
    :type v: Vec3
    :type n: Vec3
    :type ni_over_nt: float
    :return returns refracted light vector if refracted
    :rtype: (boolean, Vec3)
    """
    uv = Vec3.unit_vector(v)
    dt = Vec3.dot(uv, n)
    discriminant = 1.0 - ni_over_nt * ni_over_nt * (1 - dt*dt)
    if discriminant > 0:
        refracted = ni_over_nt * (uv - n*dt) - n * math.sqrt(discriminant)
        return True, refracted
    else:
        return False, None


def schlick(cosine, ref_idx):
    r0 = (1-ref_idx) / (1+ref_idx)
    r0 = r0*r0
    return r0 + (1-r0) * math.pow((1-cosine), 5)


class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = fuzz

    def scatter(self, r_in, rec):
        reflected = reflect(Vec3.unit_vector(r_in.direction), rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz * random_in_unit_sphere())
        attenuation = self.albedo
        return Vec3.dot(scattered.direction, rec.normal) > 0, scattered, attenuation


class Dielectric(Material):
    def __init__(self, ri):
        self.ref_idx = ri

    def scatter(self, r_in, rec):
        reflected = reflect(r_in.direction, rec.normal)
        attenuation = Vec3(1.0, 1.0, 1.0)
        if Vec3.dot(r_in.direction, rec.normal) > 0:
            outward_normal = -rec.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * Vec3.dot(r_in.direction, rec.normal) / Vec3.length(r_in.direction)
        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0 / self.ref_idx
            cosine = -Vec3.dot(r_in.direction, rec.normal) / Vec3.length(r_in.direction)

        is_refracted, refracted = refract(r_in.direction, outward_normal, ni_over_nt)
        if is_refracted:
            reflect_prob = schlick(cosine, self.ref_idx)
        else:
            scattered = Ray(rec.p, reflected)
            reflect_prob = 1.0

        if random() < reflect_prob:
            scattered = Ray(rec.p, reflected)
        else:
            scattered = Ray(rec.p, refracted)

        return True, scattered, attenuation


class Camera:
    def __init__(self):
        self.lower_left_corner = Vec3(-2.0, -1.0, -1.0)
        self.horizontal = Vec3(4.0, 0.0, 0.0)
        self.vertical = Vec3(0.0, 2.0, 0.0)
        self.origin = Vec3(0.0, 0.0, 0.0)

    def get_ray(self, u, v):
        return Ray(self.origin, self.lower_left_corner + self.horizontal * u + self.vertical * v - self.origin)


def color(r, world, depth):
    """
    :type r: Ray
    :type world: Hitable
    :type depth: int
    :return: color at the given intersection point
    """

    rec = world.hit(r, 0.001, 999999)
    if rec is not None:
        res, scattered, attenuation = rec.material.scatter(r, rec)
        if depth < 50 and res:
                return attenuation * color(scattered, world, depth+1)
        else:
            return Vec3(0, 0, 0)
    else:
        unit_direction = Vec3.unit_vector(r.direction)
        t = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)


def random_in_unit_sphere():
    while True:
        rand_vec = Vec3(random(), random(), random())
        p = rand_vec * 2.0 - Vec3(1.0, 1.0, 1.0)
        if Vec3.squared_length(p) < 1.0:
            return p


def make_color(r0, g0, b0):
    return '#{0:02x}{1:02x}{2:02x}'.format(r0, g0, b0)


def save_image(img, format):
    import os
    img.write(os.path.basename(__file__).split('.')[0] + '.' + format, format=format)


if __name__ == '__main__':
    nx = 200
    ny = 100
    ns = 100

    from tkinter import *

    main = Tk()
    w = Canvas(main, width=nx, height=ny)
    w.pack()

    world = HitableList([
        Sphere(Vec3( 0,      0, -1), 0.5, material=Lambertian(Vec3(0.1, 0.2, 0.5))),
        Sphere(Vec3( 0, -100.5, -1), 100, material=Lambertian(Vec3(0.8, 0.8, 0.0))),
        Sphere(Vec3( 1,      0, -1), 0.5, material=Metal(Vec3(0.8, 0.6, 0.2), fuzz=0.3)),
        Sphere(Vec3(-1,      0, -1), 0.5, material=Dielectric(1.5)),
        Sphere(Vec3(-1,      0, -1), -0.45, material=Dielectric(1.5)),
    ])
    cam = Camera()

    img = PhotoImage(width=nx, height=ny)

    for j in range(ny):
        for i in range(nx):
            col = Vec3(0, 0, 0)
            for s in range(ns):
                u = float(i + random()) / float(nx)
                v = float(j + random()) / float(ny)
                r = cam.get_ray(u, v)
                col += color(r, world, 0)
            col /= float(ns)
            col = Vec3(math.sqrt(col.r), math.sqrt(col.g), math.sqrt(col.b))
            ir = int(255.99 * col.r)
            ig = int(255.99 * col.g)
            ib = int(255.99 * col.b)
            c = make_color(ir, ig, ib)
            img.put(c, (i, ny-j))

    w.create_image((nx/2, ny/2), image=img, state="normal")

    save_image(img, 'ppm')

    mainloop()
