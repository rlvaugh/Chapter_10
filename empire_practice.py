"""Galaxy simulator with empire expansion rings"""
import tkinter as tk
from random import randint
import math
import time

#=============================================================================
# MAIN INPUT

# location of galactic empire homeworld on map:
HOMEWORLD_LOC = (0, 0)

# maximum number of years to simulate:
MAX_YEARS = 10000000

# average expansion velocity as fraction of speed of light:
SPEED = 0.005

# scale units
UNIT = 200

#==============================================================================

# actual Milky Way Dimensions (light-years)
DISC_RADIUS = 50000

# display parameters
disc_radius_scaled = round(DISC_RADIUS/UNIT)
fuzz = int(0.030 * disc_radius_scaled) # randomly shift star locations

# set-up display canvas
root = tk.Tk()
root.title("Milky Way galaxy")
c = tk.Canvas(root, width=1200, height=800, bg='black')
c.grid()
c.configure(scrollregion=(-600, -400, 600, 400))

def spirals(b, r, rot_fac, fuz_fac, arm):
    """Build spiral arms for tkinter display using Logarithmic spiral formula.

    b = arbitrary constant in logarithmic spiral equation
    r = scaled galactic disc radius
    rot_fac = rotation factor
    fuz_fac = random shift in star position in arm, applied to 'fuzz' variable
    arm = spiral arm (0 = main arm, 1 = trailing stars)
    """
    spiral_stars = []
    for i in range(0, 650, 2): # use range(0, 1000, 2) for no black hole
        theta = math.radians(i)
        x = r * math.exp(b*theta) * math.cos(theta + math.pi * rot_fac)\
            + randint(-fuzz, fuzz) * fuz_fac
        y = r * math.exp(b*theta) * math.sin(theta + math.pi * rot_fac)\
            + randint(-fuzz, fuzz) * fuz_fac
        spiral_stars.append((x, y))
    for x, y in spiral_stars:
        if arm == 0 and int(x % 2) == 0:
            c.create_oval(x-2, y-2, x+2, y+2, fill='white', outline='')
        elif arm == 0 and int(x % 2) != 0:
            c.create_oval(x-1, y-1, x+1, y+1, fill='white', outline='')
        elif arm == 1:
            c.create_oval(x, y, x, y, fill='white', outline='')

def star_haze(scalar):
    """Randomly distribute faint tkinter stars in galactic disc.

    scalar = multiplier to vary number of stars posted
    """
    haze = []
    for i in range(0, disc_radius_scaled * scalar):
        x = randint(-disc_radius_scaled, disc_radius_scaled)
        y = randint(-disc_radius_scaled, disc_radius_scaled)
        distance_from_center = math.sqrt(x**2 + y**2)
        if distance_from_center < disc_radius_scaled:
            haze.append((x, y))
            c.create_text(x, y, fill='white', font=('Helvetica', '7'), text='.')

def main():
    """Generate galaxy display, call MCS function, post results."""
    # build spiral arms and haze
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=1.91, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-2.09, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.4, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.6, fuz_fac=1.5, arm=1)
    star_haze(scalar=5)

    # model empire expansion from homeworld
    r = 0 # radius from homeworld
    text_y_loc = -290
    x, y = HOMEWORLD_LOC
    c.create_oval(x-5, y-5, x+5, y+5, fill='red')
    increment = round(MAX_YEARS / 10)# year interval to post circles
    c.create_text(-500, -350, anchor='w', fill='red', text='Increment = {:,}'
                  .format(increment))
    c.create_text(-500, -325, anchor='w', fill='red',
                  text='Velocity as fraction of Light = {:,}'.format(SPEED))
    
    for years in range(0, MAX_YEARS + 1, increment):
        time.sleep(0.5) # delay before posting new expansion circle
        traveled = SPEED * increment / UNIT
        r = r + traveled
        c.create_oval(x-r, y-r, x+r, y+r, fill='', outline='red', width='2')
        c.create_text(-500, text_y_loc, anchor='w', fill='red',
                      text='Years = {:,}'.format(years))
        text_y_loc += 20
        # update canvas for new circle; no longer need mainloop()
        c.update_idletasks()
        c.update()

if __name__ == '__main__':
    main()
