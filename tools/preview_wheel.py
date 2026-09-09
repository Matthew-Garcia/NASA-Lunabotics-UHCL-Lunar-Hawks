"""Orthographic z-buffer render of the actual STL; requires trimesh, numpy, Pillow."""
from pathlib import Path
import numpy as np
import trimesh
from PIL import Image
root=Path(__file__).resolve().parents[1]
m=trimesh.load_mesh(root/'cad/full_rover/wheel.stl')
m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
view=np.array([.48,-.80,.36]);view/=np.linalg.norm(view)
right=np.cross([0,0,1],view);right/=np.linalg.norm(right);up=np.cross(view,right)
v=m.vertices@np.array([right,up,view]).T
v[:,:2]*=2.5;v[:,0]+=500;v[:,1]=500-v[:,1]
buf=np.full((1000,1000),-np.inf);rgb=np.full((1000,1000,3),255,dtype=np.uint8)
light=np.array([-.3,-.7,.65]);light/=np.linalg.norm(light)
for face,normal in zip(m.faces,m.face_normals):
 t=v[face];lo=np.maximum(np.floor(t[:,:2].min(0)).astype(int),0);hi=np.minimum(np.ceil(t[:,:2].max(0)).astype(int),999)
 if np.any(lo>hi):continue
 x,y=np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5)
 a,b,c=t;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
 if abs(den)<1e-9:continue
 u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den
 w=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den
 z=u*a[2]+w*b[2]+(1-u-w)*c[2]
 region=buf[lo[1]:hi[1]+1,lo[0]:hi[0]+1];mask=(u>=-1e-7)&(w>=-1e-7)&(u+w<=1+1e-7)&(z>region)
 region[mask]=z[mask]
 color=np.array([185,62,45])*np.clip(.65+.35*np.dot(normal,light),.3,1)
 rgb[lo[1]:hi[1]+1,lo[0]:hi[0]+1][mask]=color.astype(np.uint8)
Image.fromarray(rgb).save(root/'cad/full_rover/wheel_preview.png')
