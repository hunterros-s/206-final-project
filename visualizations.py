
# passing attempts vs condition (side by side box and whisker plot, x axis: condition, y axis: attempts)
import matplotlib.pyplot as plt
import re

def make_graphics(data):
    # temperature vs attendance (line chart, x axis temp, y axis average attendance)
    temp_vs_attendance = {}
    for row in data:
        # 401220119, 'http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401220119?lang=en&region=us', '2020-09-27T17:00Z', 'Los Angeles Rams at Buffalo Bills', 0, 0, 0, 'Orchard Park, NY 14127', '23-32', '24-33', '1/2', 30, '0/0', 0, 2368, 2368, 10, 68, 'Fair'
        _, _, _, game, attendance, _, _, _, _, _, _, _, _, _, _, _, _, temp, _ = row

        name = re.search(r'.*at (.*)', game).group(1)

        if attendance == 0:  # ignoring covid games
            continue

        if name not in temp_vs_attendance:
            temp_vs_attendance[name] = []
        
        temp_vs_attendance[name].append(
            (temp, attendance)
        )
    temp_attendance(temp_vs_attendance)

    # condition vs attendance (violin chart, x axis condition, y axis average attendance)
    condition_vs_attendance = {}
    for row in data:
        # id, ref, iso, name, attendance, grass, indoor, location, first_team_comp, second_teamp_comp, first_kicking_fg, first_kicking_long, second_kicking_fg, second_kicking_long, weather_id, weather_id, wspd, temp, condition
        _, _, _, _, attendance, _, _, _, _, _, _, _, _, _, _, _, _, _, condition = row

        if attendance == 0:  # ignoring covid games
            continue

        if condition not in condition_vs_attendance:
            condition_vs_attendance[condition] = []
        
        condition_vs_attendance[condition].append(attendance)
    
    # remove conditions that don't have a lot of data
    conditons_to_remove = []
    for condition, attendance_list in condition_vs_attendance.items():
        if len(attendance_list) < 10:
            conditons_to_remove.append(condition)
    for condition in conditons_to_remove:
        del condition_vs_attendance[condition]

    condition_attendance(condition_vs_attendance)

    # wspd vs kicking (attempts, long, pct) -- (dot plot, x: wspd, y: longest fg)
    wspd_x, long_y = [], []
    for row in data:
        # id, ref, iso, name, attendance, grass, indoor, location, first_team_comp, second_teamp_comp, first_kicking_fg, first_kicking_long, second_kicking_fg, second_kicking_long, weather_id, weather_id, wspd, temp, condition
        _, _, _, _, _, _, _, _, _, _, _, first_kicking_long, _, second_kicking_long, _, _, wspd, _, _ = row

        if first_kicking_long > 0:
            wspd_x.append(wspd)
            long_y.append(first_kicking_long)
        
        if second_kicking_long > 0:
            wspd_x.append(wspd)
            long_y.append(second_kicking_long)
    wspd_long(wspd_x, long_y)


    wspd_x, attempts_y = [], []
    for row in data:
        # id, ref, iso, name, attendance, grass, indoor, location, first_team_comp, second_teamp_comp, first_kicking_fg, first_kicking_long, second_kicking_fg, second_kicking_long, weather_id, weather_id, wspd, temp, condition
        _, _, _, _, _, _, _, _, first_team_comp, second_teamp_comp, _, _, _, _, _, _, wspd, _, _ = row

        f_completions, f_attempts = first_team_comp.split("-")
        s_completions, s_attempts = second_teamp_comp.split("-")

        f_attempts = int(f_attempts)
        s_attempts = int(s_attempts)

        wspd_x.append(wspd)
        attempts_y.append(f_attempts)

        wspd_x.append(wspd)
        attempts_y.append(s_attempts)
    wspd_attempts(wspd_x, attempts_y)

def wspd_attempts(wspd_x, attempts_y):
    occurrences = {}

    # Count the occurrences of each (wspd, long_fg) pair
    for wspd, attempt in zip(wspd_x, attempts_y):
        occurrences[(wspd, attempt)] = occurrences.get((wspd, attempt), 0) + 1

    # Now generate the sizes for the scatterplot based on the occurrences
    # You can adjust the multiplication factor to get the desired effect for the dot sizes
    sizes = [20 * occurrences[(wspd, attempt)] for wspd, attempt in zip(wspd_x, attempts_y)]

    # Create the scatter plot with dynamic sizes
    plt.figure()
    plt.scatter(wspd_x, attempts_y, s=sizes)

    # Adding labels for clarity
    plt.xlabel('Wind Speed (mph)')
    plt.ylabel('Number of passing attempts')
    plt.title('Number of passing attempts vs Wind Speed')

    # Display the plot
    plt.show()
    plt.savefig("wspd_vs_passing.png")

def wspd_long(wspd_x, long_y):
    # Dictionary to count occurrences of (wspd, long_fg) pairs, where the key will
    # be a tuple (wspd, long_fg) and the value is the count
    occurrences = {}

    # Count the occurrences of each (wspd, long_fg) pair
    for wspd, long_fg in zip(wspd_x, long_y):
        occurrences[(wspd, long_fg)] = occurrences.get((wspd, long_fg), 0) + 1

    # Now generate the sizes for the scatterplot based on the occurrences
    # You can adjust the multiplication factor to get the desired effect for the dot sizes
    sizes = [20 * occurrences[(wspd, long_fg)] for wspd, long_fg in zip(wspd_x, long_y)]

    # Create the scatter plot with dynamic sizes
    plt.figure()
    plt.scatter(wspd_x, long_y, s=sizes)

    # Adding labels for clarity
    plt.xlabel('Wind Speed (mph)')
    plt.ylabel('Longest Field Goal (yards)')
    plt.title('Longest Field Goals vs Wind Speed')

    # Display the plot
    plt.show()
    plt.savefig("wspd_vs_fg_long.png")


def condition_attendance(data):
    # Extracting condition names and corresponding attendances
    conditions = list(data.keys())
    all_attendances = [data[cond] for cond in conditions]
    
    # Creating the violin plot
    plt.figure(figsize=(12, 8))
    plt.violinplot(all_attendances, showmeans=False, showextrema=True, showmedians=True)
    
    # Setting x-axis ticks to match conditions
    plt.xticks(range(1, len(conditions) + 1), conditions, rotation=45)
    
    # Adding labels and a title to the plot
    plt.xlabel('Condition')
    plt.ylabel('Attendance')
    plt.title('Violin Plot of Attendance by Condition')
    
    # Displaying the plot
    plt.tight_layout()  # Adjusts plot parameters to give some padding
    plt.show()
    plt.savefig("condition_vs_attendance.png")

colors = [
    "#377eb8", "#ff7f00", "#4daf4a", "#f781bf", 
    "#a65628", "#984ea3", "#999999", "#e41a1c", 
    "#dede00", "#f0027f", "#1b9e77", "#d95f02", 
    "#7570b3", "#66a61e", "#e7298a", "#e6ab02", 
    "#a6761d", "#666666", "#1b70fc", "#f0052e", 
    "#4eae52", "#bc5ef1", "#fffe54", "#ff2fad", 
    "#005603", "#980056", "#f6ef00", "#00396b", 
    "#0066fa", "#ffb000", "#00abae", "#aba000",
]

def temp_attendance(data):
    plt.figure(figsize=(14, 8))

    for index, (team, temp_att_list) in enumerate(sorted(data.items())):
        temp, attendance = zip(*temp_att_list)
        
        # Assign colors to teams by using the index to access the color list
        color = colors[index % len(colors)]
        plt.scatter(temp, attendance, color=color, label=team)

    plt.title('Temperature vs Attendance by Team')
    plt.xlabel('Temperature (°F)')
    plt.ylabel('Attendance')

    # Increase the number of columns in the legend and shrink the plot to fit
    legend = plt.legend(title='Team', bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)

    # Shrink the plot's width to make space for the legend
    plt.subplots_adjust(right=0.65)

    plt.tight_layout()
    plt.show()
    plt.savefig('temp_vs_attendance.png')
