# Copyright (C) 2011 Marie E. Rognes
#
# This file is part of DOLFIN.
#
# DOLFIN is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DOLFIN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DOLFIN. If not, see <http://www.gnu.org/licenses/>.
#
# First added:  2011-11-09
# Last changed: 2012-08-06

# Begin demo

from dolfin import *

# Create classes for defining parts of the interior of the domain
class Left(SubDomain):
    def inside(self, x, on_boundary):
        return (x[0] < 0.3)

class Mid(SubDomain):
    def inside(self, x, on_boundary):
        return (x[0] >= 0.3) and (x[0] <= 0.7)

class Right(SubDomain):
    def inside(self, x, on_boundary):
        return (x[0] > 0.7)

# Initialize sub-domain instances
left = Left()
mid = Mid()
right = Right()

# Define mesh
mesh = UnitSquareMesh(64, 64)

# Initialize mesh function for interior domains
domains = CellFunction("size_t", mesh)
domains.set_all(0)
left.mark(domains, 1)
mid.mark(domains, 2)
right.mark(domains, 3)

# Define input data
cell = mesh.ufl_cell()
alpha = Constant(1e-3)
f = Constant(3.0)
g = Constant(5.0)

# Define function space and basis functions
V = FunctionSpace(mesh, "CG", 2)
u = TrialFunction(V)
v = TestFunction(V)

# TODO: Make a nicer PyDOLFIN integration of Domain and Mesh,
# e.g. passing mesh to Domain, or making Mesh a subclass of Domain,
# or associating domains with Domain instead of the measure.
D = Domain(cell, "MyDomain")
DL = Region(D, (1,2), "LeftAndMid")
DM = Region(D, (2,), "Mid")
DR = Region(D, (2,3), "RightAndMid")

# Define new measures associated with the interior domains
dx = Measure("dx")[domains]

# Make forms for equation
a = alpha*dot(grad(u), grad(v))*dx() + u*v*dx()
L = f*v*dx(DR) + g*v*dx(DL) - (f+g)/2*v*dx(DM)

# Solve problem
u = Function(V)
solve(a == L, u)

# Evaluate integral of u over each subdomain and region
regions = (0, 1, 2, 3, DR, DL, DM, D)
for R in regions:
    m2 = u*dx(R)
    v2 = assemble(m2)
    print "\int u dx(%s) = %s" % (R, v2)

# Plot solution and gradient
if 1:
    plot(u, title="u")
    plot(grad(u), title="Projected grad(u)")
    interactive()