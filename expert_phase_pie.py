import plotly.express as px

def getChart(studies):
    # group by items in studies for "phase" and count the number of studies in each phase
    phase_dist = studies.groupby('phase').size().reset_index(name='counts')
    # print(phase_dist.head())

    # create a new column for the percentage of studies in each phase
    phase_dist['percent'] = round(phase_dist['counts']/phase_dist['counts'].sum()*100, 2)
    # print(phase_dist.head())
    

    # plot pie chart of the percentage distribution of studies in each phase
    expert_pie_phase = px.pie(phase_dist, values='percent', names='phase', title='Percentage Distribution of Studies in Each Phase',
                              hover_data=['counts'], labels={'counts':'#studies'})
    return expert_pie_phase








