import plotly.graph_objs as go
import pandas as pd
# from sqlalchemy import create_engine

# engine = create_engine(
#       "mysql+mysqlconnector://root:abc123@localhost/ujiantitanic?host=localhost?port=3306")

# conn = engine.connect()

# results = conn.execute("SELECT * from titanic").fetchall()
# dfTitanic = pd.DataFrame(results)
# dfTitanic.columns = results[0].keys()

# results = conn.execute("SELECT * from titanicoutcalc").fetchall()
# dfTitanicOutCalc = pd.DataFrame(results)
# dfTitanicOutCalc.columns = results[0].keys()

# results = conn.execute("SELECT * from titanic t join titanicoutcalc toc on t.outliercalcId = toc.id").fetchall()
# dfJoin = pd.DataFrame(results)
# dfJoin.columns = results[0].keys()

df = pd.read_csv('bank-fixed-column.csv');
dfFilled = pd.read_csv('bankM.csv');
# dfJoin = pd.merge(dfTitanic, dfTitanicOutCalc, left_on='outliercalcId', right_on='id');

dfDict = {
    'bank': df,
    'bankFill': dfFilled,
}

listGOFunc = {
    "bar": go.Bar,
    "violin": go.Violin,
    "box": go.Box
}
def getPlot(table, jenis, xCategory, yCategory) :
    return [
            listGOFunc[jenis](
                x=dfDict[table][xCategory],
                y=dfDict[dfDict['got_loan']==1][yCategory],
                # text=dfDict[table]['deck'],
                opacity=0.7,
                name=1,
                marker=dict(color='blue')
            ),
            listGOFunc[jenis](
                x=dfDict[table][xCategory],
                y=dfDict[dfDict['got_loan']==2][yCategory],
                # text=dfDict[table]['deck'],
                opacity=0.7,
                name=2,
                marker=dict(color='orange')
            )]