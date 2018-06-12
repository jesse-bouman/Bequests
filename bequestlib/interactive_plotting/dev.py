import plotly.graph_objs as go


def make_component_plot(df):
    df2 = df
    print(df2['bins'])
    df2['bins'] = df2['bins'].map(lambda xi: f'[-0.5, 0]' if not type(xi) == str else xi)
    df2['vals'] = df2['bins'].map(lambda xi: (float(xi.split(',')[0][1:]) + float(xi.split(',')[1][1:-1])) / 2)
    df2 = df2.fillna(0)
    df2 = df2.groupby(['Reporting_Year', 'vals', 'measure'], as_index=False).sum()
    combinations = df2.groupby(['Reporting_Year', 'measure'], as_index=False).sum()
    combs = []
    for i, row in combinations.iterrows():
        combs.append((row['Reporting_Year'], row['measure']))
    data = []
    first_year, first_measure = combs[0]
    for year, measure in combs:
        visible = (first_measure == measure)
        opacity = 0.1 + 0.9 * (first_year == year)
        ss = df2[df2['Reporting_Year'] == year]
        ss = ss[ss['measure'] == measure].copy()
        x = ss['vals']
        y = ss['Ead_Ifrs9']
        data.append(go.Bar(x=x, y=y, width=0.005, visible=visible, opacity=opacity, name=year))
    steps = []

    for i, year in enumerate(df2['Reporting_Year'].unique()):
        opacity_ind = [0.1 + 0.9*(y == year) for y, m in combs]
        step = dict(
            label=year,
            method='restyle',
            args=['opacity', opacity_ind],
        )
        # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Reporting Year: "},
        pad={"t": 50},
        steps=steps
    )]

    buttons = []
    for i, measure in enumerate(df2['measure'].unique()):
        visibility_ind = [m == measure for y, m in combs]
        button = dict(
            args=['visible', visibility_ind],
            label=measure,
            method='restyle'
        )
        buttons.append(button)

    updatemenus = list([
        dict(
            buttons=buttons,
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0.1,
            xanchor='left',
            y=1.1,
            yanchor='top'
        ),
    ])

    layout = dict(sliders=sliders, updatemenus=updatemenus, title='Component breakdown')
    fig = dict(data=data, layout=layout)
    return fig
