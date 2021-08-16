import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image

# Read the image
image = Image.open('timsburylake.jpg')

# Set image dimensions, image resolution and grid size
width, height = image.size
my_dpi=300.
part = 50  

fig=plt.figure(figsize=(float(image.size[0])/my_dpi,float(image.size[1])/my_dpi),dpi=my_dpi)
ax=fig.add_subplot(111)

# Set up figure
def figure_setup():

    # Remove whitespace from around the image
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

    # Set the gridding interval
    gridInterval_x= width*1.0 / part
    gridInterval_y= height*1.0 / part
    # for integer or float tickers in the xy axis
    loc_x = plticker.MultipleLocator(base=gridInterval_x)   
    loc_y = plticker.MultipleLocator(base=gridInterval_y)
    ax.xaxis.set_major_locator(loc_x)
    ax.yaxis.set_major_locator(loc_y)

    # Add the grid
    ax.grid(which='major', axis='both', linestyle='-', color='r')

    # Add the image
    ax.imshow(image)

    # Find the number of gridsquares in x and y coordinates
    nx=abs(int(float(ax.get_xlim()[1]-ax.get_xlim()[0])/float(gridInterval_x)))
    ny=abs(int(float(ax.get_ylim()[1]-ax.get_ylim()[0])/float(gridInterval_y)))

    return nx, ny, gridInterval_x, gridInterval_y

nx, ny, gridInterval_x, gridInterval_y = figure_setup()

# Add labels to the gridsquares
def grid_labels(labelInterval=100.):
    for i in range(ny):
        y=labelInterval/2+i*gridInterval_y
        for j in range(nx):
            x=gridInterval_x/2.+float(j)*gridInterval_x
            label = ax.text(x,y,'{:d}'.format(j+i*nx),color='b',ha='center',va='center',fontsize=5)
    return label

# Save the figure
def save_image():
    grid_labels()
    fig.savefig('lake-grid.png',dpi=my_dpi)

save_image()
