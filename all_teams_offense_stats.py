import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, CheckButtons
import matplotlib.image as mpimg

from pathlib import Path
import cv2


global cur_team

team_dict = {
    'ARI': '#97233F',
    'ATL': '#A71930',
    'BAL': '#241773',
    'BUF': '#00338D',
    'CAR': '#0085CA',
    'CHI': '#C83803',
    'CIN': '#FB4F14',
    'CLE': '#FF3C00',
    'DAL': '#041E42',
    'DEN': '#FB4F14', # denver broncos
    'DET': '#0076B6', # detroit lions
    'GB': '#203731',# green bay packers
    'HOU': '#E60029', # houston texanas
    'IND': '#002C5F', # indiana colts
    'JAX': '#006778', # jacksonville jaguars
    'KC': "#E31837",# kansas city chiefs
    'LA': '#003594',# los angeles rams
    'LAC': '#0080C6', # los angeles chargers
    'LV': "#000000",# las vegas raiders
    'MIA': '#008E97', # miami dolphins
    'MIN': '#4F2683', # minnesota vikings
    'NE': '#002244',# new england patriots
    'NO': '#D3BC8D',# new orleans saints
    'NYG': '#0D2266', # new york giants
    'NYJ': '#125740', # new york jets
    'PHI': '#2B8C4E', # philadelphia eagles
    'PIT': '#FFB612', # pittsburg steelers
    'SEA': '#002244', # seattle seahawks
    'SF': '#AA0000', # san francisco 49ers
    'TB': '#A71930', # tampa bay bucaneers
    'TEN': '#0C2340', # tennessee titans
    'WAS': '#5A1414', # washington football team
}

# --- Process user input ---
'''
user_in= ''
while user_in not in team_dict.keys():
    user_in = input("What team would you like to view stats for?: ")
    user_in = user_in.upper()

    if user_in not in team_dict.keys():
        print('Team not found. Use the teams geographical shortening. i.e.team TEN, PHI, SF, etc...')


print('Input recieved')
'''
user_in = 'KC' # default pick
# --- Create plot ---

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3)

x = range(2012, 2026)
#l, = ax.plot(x)

# read csv file
folder = Path(r"C:\Users\savag\Documents\Coding\data_analysis\nfl_stats_analysis\data")
file_path = folder / "yearly_team_stats_offense.csv"

df = pd.read_csv(file_path)
df = df.loc[df['season_type'] == 'REG'] # isolate regular season stats only

# create radio button section
ax_radio = plt.axes([0.01, 0.4, 0.11, 0.15], facecolor='lightgoldenrodyellow')
#ax_radio.set_aspect('equal')
radio = RadioButtons(ax_radio, ('passing yards', 
                                'rushing yards', 
                                'passing touchdowns', 
                                'rushing touchdowns', 
                                'third down', 
                                'fourth down', 
                                'pass adot', 
                                'interceptions', 
                                'yards/snap'))

# create team select button section
team_sel_ax = plt.axes([0.01, 0.05, 0.20, 0.26], facecolor='lightgoldenrodyellow')
team_radio = RadioButtons(team_sel_ax, list(team_dict.keys()), layout=(16, 2))

# display team logo
logo_folder = Path(r"C:\Users\savag\Documents\Coding\data_analysis\nfl_stats_analysis\logos")
logo_file_path = logo_folder / f"{user_in}.png"

logo_ax = plt.axes([0.01, 0.6, 0.36, 0.20])

#print(f'Trying to open image at: {logo_file_path}')

img = mpimg.imread(logo_file_path)
logo_ax.imshow(img)
logo_ax.axis('off')

'''
# 1. Load the image (OpenCV loads as BGR by default)
img = cv2.imread(logo_file_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 2. Resize it
resized_img = cv2.resize(img_rgb, (1100, 900))

logo_ax.imshow(resized_img)
logo_ax.axis('off')
'''
logo_ax.text(300,680, user_in, 
        bbox=dict(facecolor='#ffffff', edgecolor='#ffffff',alpha=0.5, boxstyle='square'))

# --- Calculate league average statistics each year ---
league_avg_ints = []
league_avg_passing_yds = []
league_avg_rushing_yds = []
league_avg_passing_td = []
league_avg_rushing_td = []

for i in range(2012, 2026):
    total_ints = 0
    total_passing_yds = 0
    total_rushing_yds = 0
    total_passing_td = 0
    total_rushing_td = 0

    szn = df[df['season']==i]

    for idx, row in szn.iterrows():
        total_ints += row['interception']
        total_passing_yds += row['passing_yards']
        total_rushing_yds += row['rushing_yards']
        total_passing_td += row['pass_touchdown']
        total_rushing_td += row['rush_touchdown']
    
    avg_ints = total_ints / 32
    avg_passing_yds = total_passing_yds / 32
    avg_rush_yds = total_rushing_yds / 32
    

    league_avg_ints.append(avg_ints)
    league_avg_passing_yds.append(avg_passing_yds)
    league_avg_rushing_yds.append(avg_rush_yds)
    league_avg_passing_td.append(total_passing_td/32)
    league_avg_rushing_td.append(total_rushing_td/32)

    #print(f'Avg interceptions for {i} season: {avg}\n')


# display passing yards by default
l0, = ax.plot(x, list(df.loc[(df['team']==user_in)]['passing_yards']), visible=True, color=team_dict[user_in], label=user_in)
ax.plot(x, league_avg_passing_yds, color='#000000', linestyle='dashed', label='League Avg')

# set y-axis to be relative to values across all teams
all_vals = (df['passing_yards']).tolist()
ax.set_ylim(min(all_vals), max(all_vals))

ax.legend()

cur_team = user_in

def change_plot(lbl, team=None):
    global cur_team

    if not team:
        team = cur_team


    ax.clear()
    plt.gca().autoscale(enable=True, axis='y') # reset to default autoscaling for y-axis
    #ax.legend()

    if lbl == 'passing yards':
        ax.plot(x, list(df.loc[(df['team']==team)]['passing_yards']), color=team_dict[team], label=team)
        ax.plot(x, league_avg_passing_yds, color='#000000', linestyle='dashed', label='League Avg')

        # set y-axis to be relative to values across all teams
        all_vals = (df['passing_yards']).tolist()
        ax.set_ylim(min(all_vals), max(all_vals))
    
    elif lbl == 'rushing yards':
        ax.plot(x, list(df.loc[(df['team']==team)]['rushing_yards']), color=team_dict[team], label=team)
        ax.plot(x, league_avg_rushing_yds, color='#000000', linestyle='dashed', label='League Avg')

        # set y-axis to be relative to values across all teams
        all_vals = (df['rushing_yards']).tolist()
        ax.set_ylim(min(all_vals), max(all_vals))

    elif lbl == 'passing touchdowns':
        ax.plot(x, list(df.loc[(df['team']==team)]['pass_touchdown']), color=team_dict[team], label=team)
        ax.plot(x, league_avg_passing_td, color='#000000', linestyle='dashed', label='League Avg')

        # set y-axis to be relative to values across all teams
        all_vals = (df['pass_touchdown']).tolist()
        ax.set_ylim(min(all_vals), max(all_vals))
    
    elif lbl == 'rushing touchdowns':
        ax.plot(x, list(df.loc[(df['team']==team)]['rush_touchdown']), color=team_dict[team], label=team) 
        ax.plot(x, league_avg_rushing_td, color='#000000', linestyle='dashed', label='League Avg')

        # set y-axis to be relative to values across all teams
        all_vals = (df['rush_touchdown']).tolist()
        ax.set_ylim(min(all_vals), max(all_vals))
    
    elif lbl == 'third down':
        ax.plot(x, list(df.loc[(df['team']==team)]['third_down_converted']), color=team_dict[team], label='Converted')
        ax.plot(x, list(df.loc[(df['team']==team)]['third_down_failed']), color='#ff0000', linestyle='dashed', label='Failed')
        
        '''
        # set y-axis to be relative to values across all teams
        all_vals = (df['third_down_failed']).tolist()
        ax.set_ylim(min(all_vals), max(all_vals))
        '''

    elif lbl == 'fourth down':
        ax.plot(x, list(df.loc[(df['team']==team)]['fourth_down_converted']), color="#000000", label='Converted')
        ax.plot(x, list(df.loc[(df['team']==team)]['fourth_down_failed']), color="#ff0000", linestyle='dashed', label='Failed')
        ax.plot(x, (df.loc[df['team']==team]['fourth_down_converted'] + df.loc[df['team']==team]['fourth_down_failed']).tolist(), color=team_dict[team], label='Total')

    
    elif lbl =='pass adot':
        ax.plot(x, list(df.loc[(df['team']==team)]['pass_adot']), color=team_dict[team], label=team)

        # set y-axis to be relative to values across all teams
        all_vals = (df['pass_adot']).tolist()
        ax.set_ylim(min(all_vals), max(all_vals))
    
    elif lbl == 'interceptions':
        ax.plot(x, list(df.loc[(df['team']==team)]['interception']), color=team_dict[team], label=team)
        ax.plot(x, league_avg_ints, color='#000000', linestyle='dashed', label='League Avg')

        # set y-axis to be relative to values across all teams
        all_vals = (df['interception']).tolist()
        ax.set_ylim(min(all_vals), max(all_vals))

    elif lbl == 'yards/snap':
        ax.plot(x, (df.loc[df['team']==team]['team_offense_yards'] / df.loc[df['team']==team]['team_offense_snaps']).tolist(), color=team_dict[team], label='Yards/Snap')
        
        # set y-axis to be relative to values across all teams
        all_vals = ((df['team_offense_yards']) / (df['team_offense_snaps'])).tolist()
        ax.set_ylim(min(all_vals), max(all_vals))
        #print(f'bottom: {min(all_vals)} | top: {max(all_vals)}')


    
    fig.canvas.draw_idle()
    ax.legend()


def change_team(lbl, im_ax):
    global cur_team

    # update current team
    cur_team = lbl

    # display team logo
    logo_folder = Path(r"C:\Users\savag\Documents\Coding\data_analysis\nfl_stats_analysis\logos")
    logo_file_path = logo_folder / f"{cur_team}.png"

    #logo_ax = plt.axes([0.01, 0.6, 0.30, 0.20])
    logo_ax.cla()

    #print(f'Trying to open image at: {logo_file_path}')
    img = mpimg.imread(logo_file_path)
    logo_ax.imshow(img)

    im_ax.imshow(img)
    im_ax.axis('off')



    im_ax.text(300,680, cur_team, 
            bbox=dict(facecolor='#ffffff', edgecolor='#ffffff',alpha=0.5, boxstyle='square'))


    # set plot to default with lbl
    change_plot('passing yards', team=lbl)
    radio.set_active(0)


team_radio.on_clicked(lambda lbl: change_team(lbl, logo_ax))
radio.on_clicked(change_plot)
plt.show()
