#!/usr/bin/env python
# Author:  J Fuentes
# Contact: me@fvnts.ch

"""
    
    Heat Equation  2D
    DO NOT EDIT THIS FILE
    
    """

# --------------------------------------------------------------------------------/
import os
import time
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

from sys import *
from scipy.special import *

from matplotlib import animation
from tempfile import NamedTemporaryFile as tmp
# --------------------------------------------------------------------------------/
os.system('cls' if os.name == 'nt' else 'clear')
# --------------------------------------------------------------------------------/
class Timer(object):
    """
        time class
        """
    def __init__(self, name=None):
        self.name = name
    
    def __enter__(self):
        self.tstart = time.time()
    
    def __exit__(self, type, value, traceback):
        if self.name:
            print '[%s]' % self.name,
        m, s = divmod(time.time() - self.tstart, 60)
        h, m = divmod(m, 60)
        print ' '
        print ' > ELAPSED TIME: %d:%02d:%02d ' % (h, m ,s)
        print ' '
# --------------------------------------------------------------------------------/
class solver(object):
    """
        class which implements a finite differences scheme
        solution to the 2D heat equation
        """
    def __init__(self, dx, dy, a, kind, timesteps = 1):
        
        # mesh interval
        self.dx = dx
        self.dy = dy
        
        # diffusion constant
        self.a = a
        
        # time steps
        self.timesteps = timesteps
        
        self.dx2 = dx**2
        self.dy2 = dy**2
        
        # mesh points
        self.nx = int(1/dx)
        self.ny = int(1/dy)
        
        # largest time interval possible to assure stability
        self.dt = self.dx2 * self.dy2 / (2.0 * a * (self.dx2 + self.dy2))
        
        self.u, self.ui = self.initialize(kind)
# --------------------------------------------------------------------------------/
    def initialize(self, kind):
        
        # solution matrices
        ui = sp.zeros([self.nx, self.ny])
        u  = sp.zeros([self.nx, self.ny])
        
        # dictionary of initial conditions ui
        for i in range(self.nx):
            for j in range(self.ny):
                if kind == "strips":
                    z = jv(0,i*self.dx) + jv(2,j*self.dy)
                    if (z  <= 1.0 and z >= 0.98):
                        ui[i,j] = 1
                    elif (z  <= 1.5 and z >= 1.25):
                        ui[i,j] = 1
                elif kind  == "boomerang":
                    z = np.log(i*self.dx * j*self.dy)
                    if (z >= -3.0 and z <= -1.5 ):
                        ui[i, j] = 1
                elif kind == "wow":
                    z = np.cosh(2*i*self.dx)**(-4) + np.cosh(j*self.dy)**(-2)
                    if (z <= 1.2 and z >= 1.0):
                        ui[i, j] = 1
                    elif (z <= 0.6 and z >= 0.4):
                        ui[i, j] = 1              
                elif kind == "spook":
                    z = (np.sin(3*i*self.dx)**3 + np.sin(5*i*self.dx)**5 +
                         np.sin(7*j*self.dy)**7 + np.sin(9*j*self.dy)**9)
                    if (z <= 0.25 and z >= 0.0):
                        ui[i, j] = 1
        return u, ui
# --------------------------------------------------------------------------------/
    def evolution(self):
        self.u[1:-1,1:-1] = self.ui[1:-1,1:-1] + self.a * self.dt * (
                            ( self.ui[2:,1:-1] - 2*self.ui[1:-1,1:-1] + self.ui[:-2,1:-1] ) / self.dx2 +
                            ( self.ui[1:-1,2:] - 2*self.ui[1:-1,1:-1] + self.ui[1:-1,:-2] ) / self.dy2 )
        self.ui = self.u.copy()
# --------------------------------------------------------------------------------/
def evolution(u, ui):
    global nx, ny
    """
    compute the finite differences evolution
    """
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            uxx = ( ui[i+1,j] - 2*ui[i,j] + ui[i-1,j] ) / dx2
            uyy = ( ui[i,j+1] - 2*ui[i,j] + ui[i,j-1] ) / dy2
            # update
            u[i, j] = ui[i, j] + dt * a * (uxx + uyy)
# --------------------------------------------------------------------------------/
def record(anim, k):
    if not hasattr(anim, '_encoded_video'):
        with tmp(suffix = '.mp4') as f:
            newname = "/Users/fuentes/workspace/" + k + '_' + f.name.split("/")[-1]
            anim.save(newname,
                      fps=20,
                      extra_args=['-vcodec','libx264','-pix_fmt','yuv420p'])
    return None
# --------------------------------------------------------------------------------/
def save_animation(anim, k):
    plt.close(anim._fig)
    return record(anim, k)
# --------------------------------------------------------------------------------/
def output(hx, hy, mode, snap, steps):

    for k in mode:
    
        heat = solver(hx, hy, 0.25, k, 1)

        fig = plt.figure()
        img = plt.subplot(111)
        im = img.imshow(heat.ui,
                        cmap=plt.cm.winter,
                        interpolation='nearest',
                        origin='lower')
        im.figure = fig
        fig.colorbar(im)
    
        def animate(i, im):
            if (i % snap == 0):
                stdout.write(">> CYCLE %d/%d %s" % (i, steps, "\r"))
                stdout.flush()
            heat.evolution()
            im.set_array(heat.ui)
            return [im]

        anim = animation.FuncAnimation(fig,
                                       animate,
                                       frames = steps,
                                       fargs = (im,),
                                       interval = 30,
                                       blit = True)
        save_animation(anim, k)
# --------------------------------------------------------------------------------/
# eof
# --------------------------------------------------------------------------------/