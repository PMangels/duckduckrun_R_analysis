import pandas as pd
import os


def read_files():
    df_csv = pd.DataFrame(columns=['timestamp', 'json.Message'])

    for filename in os.listdir("./csv_files"):
        if filename.endswith(".csv"):
            new_df = pd.read_csv("./csv_files/" + filename)
            appending_df = new_df.loc[:, ['timestamp', ' "json.Message"']]
            appending_df = appending_df.rename(columns={' "json.Message"': 'json.Message'})
            df_csv = df_csv.append(appending_df, ignore_index=True)
    return df_csv


def make_str_digit_if_possible(str):
    if str.isdigit():
        dig = int(str)
    else:
        dig = str
    return dig


def parse_df(df):
    df['userId'], df['time'], df['version'], df['log'] = df['json.Message'].str.split('_').str
    df['log'] = df.log.apply(make_str_digit_if_possible)
    return df[['version', 'userId', 'timestamp', 'log']]


def scores(df):
    df = df[df.log.apply(type) != str]
    df = df[['version', 'userId', 'log']]
    return df


def actions(df):
    df = df[df.log.apply(type) == str]
    return df


def games_started(df):
    df = df[df['log'] == 'gameStarted']
    df['games'] = df.groupby(['version','userId'])['log'].transform('count')
    df = df[['version', 'userId', 'games']]
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    return df


def main():
    complete_df = read_files()
    complete_df = parse_df(complete_df)
    complete_df.sort_values(by=["version","userId","timestamp"], ascending=True, inplace=True)
    complete_df = complete_df.reset_index(drop=True)
    complete_df.to_csv("./duckduckgo.csv", index=False)
    players_df = complete_df.groupby("version").userId.agg({'Players': 'nunique'})
    players_df.to_csv("./duckduckgo_players.csv")
    scores_df = scores(complete_df)
    scores_df.to_csv("./duckduckgo_scores.csv", index=False)
    actions_df = actions(complete_df)
    actions_df.to_csv("./duckduckgo_actions.csv", index=False)
    games_started_df = games_started(actions_df)
    games_started_df.to_csv("./duckduckgo_games_started.csv", header=True)



if __name__ == "__main__":
    main()
