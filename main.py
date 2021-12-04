from flask import Flask
from flask import request, render_template
import pandas as pd
import numpy as np
from scipy import stats


app = Flask(__name__)

@app.route("/")
def index():
    data = request.args.getlist("data")
    if data:
        player = determin_player(data)
    else:
        player = ""

    return (render_template("app.html", player=player, player_stats=get_player_stats(player)))


def determin_player(data):

    nfl = pd.read_csv("combine_data_since_2000_PROCESSED_2018-04-26.csv")
    nfl_droped = nfl.drop(["Pos", "Year", "Pfr_ID", "AV", "Team", "Round", "Pick"], axis=1)

    X = nfl_droped.drop("Player", axis=1)
    X = X.values
    y = nfl_droped["Player"]
    y = y.values

    d = [float(i) for i in data]

    new_data_point = np.array(d, ndmin=2)
    distances = np.linalg.norm(X - new_data_point, axis=1)

    k = 3
    nn_ids = distances.argsort()[:k]
    nn_player = y[nn_ids]

    player = stats.mode(nn_player)
    player_1 = str(player[0])
    player_2 = player_1.replace("[", "")
    player_3 = player_2.replace("]", "")
    player_name = player_3.replace("'", "")

    return player_name

def get_player_stats(player):

    nfl = pd.read_csv("combine_data_since_2000_PROCESSED_2018-04-26.csv")
    nfl_droped = nfl.drop(["Pfr_ID", "AV"], axis=1)
    nfl_droped.set_index("Player")
    player_stats = nfl_droped[nfl_droped["Player"] == player].to_html(escape=False, index=False)

    return player_stats


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
