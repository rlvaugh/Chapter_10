"""Monte Carlo Simulator to check for overlapping radio bubbles in galaxy."""
import tkinter as tk
from random import randint
import math
from itertools import repeat
from collections import Counter


#=============================================================================
# MAIN INPUT

# diameter of radio bubble in light years (max = 500):
EM_DIAMETER = 200

# number of advanced mcs_civs from Drake's Equation:
NUM_CIVS = 100000
# number of cases to run:
NUM_CASES = 1

#==============================================================================


# limit bubble size for better model resolution
if EM_DIAMETER > 500:
    EM_DIAMETER = 500
    
# actual Milky Way Dimensions (light-years)
DISC_RADIUS = 50000
DISC_HEIGHT = 1000
HT_SCALAR = 50 # ratio of disc radius to disc height
DISC_VOL = 7853981633974.5 # cubic LY

# scale disc to radio bubble for visual model
em_vol = 4/3 * math.pi * (EM_DIAMETER/2)**3
disc_vol_scaled = DISC_VOL/em_vol
disc_radius_scaled = round((HT_SCALAR * disc_vol_scaled / math.pi)**(1/3))

# set-up display canvas
root = tk.Tk()
root.title("Milky Way galaxy")
c = tk.Canvas(root, width=1000, height=800, bg='black')
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400))

def spirals(b, r, rot_fac, fuz_fac, arm):
    """Build spiral arms for tkinter display using Logarithmic spiral formula.

    b = arbitrary constant in logarithmic spiral equation
    r = scaled galactic disc radius
    rot_fac = rotation factor
    fuz_fac = random shift in star position in arm, applied to 'fuzz' variable
    arm = spiral arm (0 = main arm, 1 = trailing stars)
    """
    spiral_stars = []
    fuzz = int(0.030 * disc_radius_scaled) # randomly shift star locations
    for i in range(520): # use range(0, 700, 2) for no black hole at center
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
        if distance_from_center <= disc_radius_scaled:
            haze.append((x, y))
            c.create_text(x, y, fill='white', font=('Helvetica', '7'),text='.')

def civ_locations(mcs_side, mcs_ht):
    """Generate location for civilization in MCS box with same vol as disc."""
    x = randint(0, mcs_side)
    y = randint(0, mcs_side)
    z = randint(0, mcs_ht)
    return x, y, z

def civ__for_display():
    """Generate  location for civilization. If outside disc regenerate."""
    x = randint(-disc_radius_scaled, disc_radius_scaled)
    y = randint(-disc_radius_scaled, disc_radius_scaled)
    distance_from_center = math.sqrt(x**2 + y**2)
    if distance_from_center > disc_radius_scaled:
        return civ__for_display()
    else:
        return x, y

def monte_carlo():
    """Simulate civilization locations using Monte Carlo simulation."""
    # calculate MCS box model dimensions
    num_civs = NUM_CIVS
    disc_vol = DISC_VOL
    disc_area = math.pi * DISC_RADIUS**2
    mcs_cell_side = round(em_vol**(1/3))
    mcs_side = round(math.sqrt(disc_area) / mcs_cell_side)
    mcs_ht = round(DISC_HEIGHT/mcs_cell_side)
    mcs_vol = mcs_side**2 * mcs_ht * mcs_cell_side**3
    vol_diff = mcs_vol / disc_vol
    print("mcs vol / disc vol =", vol_diff)

    # adjust number of civilizations for difference in volume
    num_civs = round(num_civs * vol_diff)
    print("volume-adjusted number of civilizations = ", num_civs)

    # reduce model size if >10M civilizations modeled
    if num_civs > 10000000:
        mcs_vol = mcs_vol / 4
        mcs_side = round(mcs_vol**(1/3) / mcs_cell_side)
        mcs_ht = mcs_side
        num_civs = math.ceil(num_civs / 4)
        disc_vol = DISC_VOL / 4
        print("vol-adjusted number of civilizations / 4 = ", num_civs)
    
    # run MCS
    tot_undetected = 0
    for case in range(NUM_CASES):
        print("running case", case + 1, "...")
        mcs_civs = []
        for i in repeat(None, num_civs):
            mcs_civs.append(civ_locations(mcs_side, mcs_ht))
        overlap_count = Counter(mcs_civs)
        overlap_rollup = Counter(overlap_count.values())
        num_undetected = overlap_rollup[1]
        print("number cells with only one civ = ", num_undetected)
        tot_undetected += num_undetected
        
    single_prob = 1 - (num_undetected / num_civs)
    total_prob = 1 - (tot_undetected / (NUM_CASES * num_civs))
    return single_prob, total_prob

def main():  
    """Generate galaxy display, call MCS function, post results."""
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=1.91, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-2.09, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.4, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.6, fuz_fac=1.5, arm=1)
    star_haze(scalar=7)

    # run MCS, post civilizations & stats
    single_prob, total_prob = monte_carlo()

    # display civilizations on galactic map
    oval_size = 0 # size of posted civilization on galaxy map
    display_limit = 100000 if EM_DIAMETER > 200 else 200000 if\
                    EM_DIAMETER >= 200 else 500000 if\
                    EM_DIAMETER > 50 else 1000000
    if NUM_CIVS > display_limit:
        to_display = display_limit
    else:
        to_display = (NUM_CIVS)

    display_civs = []
    for i in repeat(None, to_display):
        display_civs.append(civ__for_display())
    for x, y in display_civs:
        if NUM_CIVS > 2500:
            c.create_oval(x-oval_size, y-oval_size, x+oval_size,
                          y+oval_size, fill='red', outline='')
        else:
            c.create_text(x, y, fill='red', text='+')
    c.create_text(0, 290, fill='white', font=('Helvetica', '11'),
                  text='DISPLAYING {:,} CIVILIZATIONS'.format(to_display))

    # display statistics
    c.create_text(-455, -375, fill='white', anchor='w',
                  text='Diameter of radio bubbles = %s LY' % (EM_DIAMETER))
    c.create_text(-455, -350, fill='white', anchor='w',
                  text='Number of advanced civilizations = {:,}'
                  .format(NUM_CIVS))
    c.create_text(-455, -325, fill='white', anchor='w',
                  text='Single case probability of detection = %.4f'
                  % (single_prob))
    c.create_text(-455, -300, fill='white', anchor='w',
                  text='Probability of detection for %s case(s) = %.4f'
                  % (NUM_CASES, total_prob))
    c.create_text(0, 325, fill='white',
                  text='SHOWING FINAL SIMULATION')
    c.create_text(0, 350, fill='red',
                  text='RED = civilization')

    #run tkinter loop
    root.mainloop()

if __name__ == '__main__':
    main()
