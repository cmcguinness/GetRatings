import matplotlib.pyplot as plt
import pandas as pd


def plotter():
    # Load CSV data
    file_path = input('Ratings file: ')
    df = pd.read_csv(file_path)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Ensure Rating column is numeric
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Drop any rows where Rating is NaN (if conversion failed)
    df = df.dropna(subset=['Rating'])

    # Convert Rating to integer
    df['Rating'] = df['Rating'].astype(int)

    # Extract hour for sorting
    df['TimeSlot'] = pd.Categorical(df['TimeSlot'], categories=sorted(df['TimeSlot'].unique(),
                                                                      key=lambda x: int(x[:-2]) + (
                                                                          12 if 'PM' in x and int(
                                                                              x[:-2]) != 12 else 0)), ordered=True)


    # Daily total ratings per network
    daily_totals = df.groupby(['Date', 'Network'])['Rating'].sum().unstack()
    daily_totals.plot(kind='bar', figsize=(10, 5), title='Daily Total Ratings by Network')
    plt.ylabel('Total Ratings')
    plt.xticks(rotation=45)
    plt.legend(title='Network')
    plt.savefig('daily_totals.png')
    plt.close()

    # Aggregate ratings per show
    show_totals = df.groupby('Show')['Rating'].sum().sort_values(ascending=False)
    show_totals.plot(kind='bar', figsize=(10, 5), title='Total Ratings by Show')
    plt.ylabel('Total Ratings')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)  # Adjust bottom margin to avoid cutting off text
    plt.savefig('total_ratings_by_show.png')
    plt.close()

    # Aggregate ratings per show, per network
    for network in df['Network'].unique():
        network_shows = df[df['Network'] == network].groupby('Show')['Rating'].sum().sort_values(ascending=False)
        network_shows.plot(kind='bar', figsize=(10, 5), title=f'Total Ratings by Show - {network}')
        plt.ylabel('Total Ratings')
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.3)  # Adjust bottom margin to avoid cutting off text
        plt.savefig(f'total_ratings_by_show_{network}.png')
        plt.close()

    # Average rating across all shows
    average_rating = df.groupby('Show')['Rating'].mean().sort_values(ascending=False)
    average_rating.plot(kind='bar', figsize=(10, 5), title='Average Ratings by Show')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)  # Adjust bottom margin to avoid cutting off text
    plt.savefig('average_ratings_by_show.png')
    plt.close()

    # Average ratings per show, per network
    for network in df['Network'].unique():
        network_avg_shows = df[df['Network'] == network].groupby('Show')['Rating'].mean().sort_values(ascending=False)
        network_avg_shows.plot(kind='bar', figsize=(10, 5), title=f'Average Ratings by Show - {network}')
        plt.ylabel('Average Rating')
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.3)
        plt.savefig(f'average_ratings_by_show_{network}.png', bbox_inches='tight')
        plt.close()

    # Percentage of viewers per show in its time slot
    time_slot_totals = df.groupby(['Date', 'TimeSlot'])['Rating'].sum()
    df['TimeSlotTotal'] = df.set_index(['Date', 'TimeSlot']).index.map(time_slot_totals)
    df['Percentage'] = (df['Rating'] / df['TimeSlotTotal']) * 100

    # Pivot data for stacked bar chart
    stacked_data = df.pivot_table(index='TimeSlot', columns='Network', values='Percentage', aggfunc='mean')
    stacked_data = stacked_data.sort_index()
    ax = stacked_data.plot(kind='bar', stacked=True, figsize=(10, 5),
                           title='Percentage of Viewers per Time Slot by Network')
    plt.ylabel('Percentage of Viewers')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)
    plt.legend(title='Network', bbox_to_anchor=(0.975, 1), loc='upper left')

    # Add labels to each segment
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', label_type='center', fontsize=10, color='white')

    plt.savefig('stacked_percentage_viewers_per_timeslot.png')
    plt.close()

if __name__ == "__main__":
    plotter()
