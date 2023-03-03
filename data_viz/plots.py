from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Read in the data
cand_sentiment_df = pd.read_json('/home/abejburton/capp30122/databased_project/data/candidate_bs.json', orient='index')
cand_sentiment_df['neg'] = cand_sentiment_df['neg'] * -1
CANDIDATES = ['Kam Buckner','Chuy García',"Ja'Mal Green",'Brandon Johnson','Sophia King','Lori Lightfoot','Roderick Sawyer','Paul Vallas','Willie Wilson']
cand_sentiment_df['candidates'] = CANDIDATES

news_sentiment_df = pd.read_json('/home/abejburton/capp30122/databased_project/data/news_bs.json', orient='index')
# cand_news_sentiment_df is a little weird w formatting hopefully it works for now
cand_news_sentiment_df = pd.read_json('/home/abejburton/capp30122/databased_project/data/cand_by_newspaper_bs.json')

# TODO get article info from maddie and also most common words.
# clean_articles_df = pd.read_csv(pathlib.Path(__file__).parent.parent / clean_articles_filepath, usecols=['candidate_id', 'newspaper_id', 'url', 'date'], nrows = 50)

count_cand_df = pd.read_json('/home/abejburton/capp30122/databased_project/analysis/data/count_cand.json', orient='index')
count_cand_df.rename(columns={0:'mentions'}, inplace=True)
MENTION_LABELS = ['Kam Buckner','Chuy García',"Ja'Mal Green",'Brandon Johnson','Sophia King','Roderick Sawyer','Paul Vallas','Willie Wilson','Lori Lightfoot','Total Articles','Total Unique Articles']
count_cand_df['candidates'] = MENTION_LABELS
count_cand_df.drop(['total_num_articles_scraped'], inplace=True)
# Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

mentions = px.bar(count_cand_df, x='candidates', y='mentions', labels={'candidates':'Candidate', 'mentions':'Number of Mentions'}, title='Number of Mentions By Candidate')
sentiment = px.bar(cand_sentiment_df, x='candidates', y=['pos','neg'], labels={'candidates':'Candidate', 'value': 'Sentiment'}, title='Sentiment Scores By Candidate')
sentiment.layout.update(showlegend=False)

BODY = html.Div(children=[
    html.Div([
        html.H5(children='Mention'),
        dcc.Graph(
            id='mention_graph',
            figure=mentions
        ),
    ]),
    html.Div([
        html.H5(children='Sentiment'),
        dcc.Graph(
            id='sentiment_graph',
            figure=sentiment
        ),
    ]),
])

NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavbarBrand("dataBased: Mayoral Candidate Coverage Analysis", className="ml-2")
                    ),
                ],
                align="center"
            ),
            href="https://plot.ly",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

app.layout = html.Div(children=[NAVBAR, BODY])

if __name__ == "__main__":
    app.run_server(debug=False, port=8056)