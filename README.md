# Ray Tracer in Python 

![Final image](./raytracer.png?raw=true)

A reimplementation of `Ray Tracing in One Weekend by Peter Shirley` in Python 3 :snake:.

 - [Original ebook](http://www.realtimerendering.com/raytracing/Ray%20Tracing%20in%20a%20Weekend.pdf)
 - [Original github source](https://github.com/petershirley/raytracinginoneweekend)

Things to note for the Python implementation:
* Initially each commit is an individual step, (or a chapter in Peter's book).
* Vec3 class is a good example on operator overloading in Python, eg. left and right multiplication, different behaviour on the type of the operand. For example, you can multiple two vectors or a vector with a number.
* After introducing antialiasing in chapter 6, it is painfully slow to run with CPython. Use of PyPy 3 is recommended, where JIT compiler shows its strength. Ray tracing is naturally very repetitive and optimization leads to impressive results compared to plain interpretation. On my machine, PyPy runs chapter 9 script in 4.38 seconds, whereas CPython runs the same script in 254.87 (!) seconds.
