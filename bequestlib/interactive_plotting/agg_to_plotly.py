import os

import pandas as pd
import plotly.offline as po
from plotly import tools

from bequestlib.interactive_plotting.custom_objects import Bar, LineDivision
from bequestlib.interactive_plotting.dev import make_component_plot


class Pane:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.data_stack = []
        self.layout = dict()
        self.fig = None

    @property
    def titles(self):
        return [i['title'] for i in self.data_stack]

    def add_subplot(self, data, title=''):
        subplot = dict(
            data=data.traces,
            title=title
        )
        if len(self.data_stack) < self.n_cols * self.n_rows:
            self.data_stack.append(subplot)
        else:
            raise ValueError('Adding too many plots to predefined pane')

    def _define_figure(self):
        fig = tools.make_subplots(rows=self.n_rows, cols=self.n_cols,
                                  subplot_titles=self.titles)
        return fig

    def stack(self):
        fig = self._define_figure()
        for i, subplot in enumerate(self.data_stack):
            row = (i // self.n_cols) + 1
            col = (i % self.n_cols) + 1
            for j in subplot['data']:
                fig.append_trace(j, row, col)
            fig.layout.update(self.layout)
        self.fig = fig

    def show(self):
        po.plot(self.fig, show_link=False)

    def full_html(self):
        return po.plot(self.fig, output_type='div', show_link=False)

    def div_only(self):
        return po.plot(self.fig, output_type='div', include_plotlyjs=False)


class StagePane(Pane):
    def __init__(self):
        super().__init__(2, 3)

    @classmethod
    def from_df(cls, df):
        obj = StagePane()

        lst_ead = Bar(df, 'Ead_Eba', 'Reporting_Year', colors='Stage')
        lst_ead_airb = Bar(df, 'Ead_Airb', 'Reporting_Year', colors='Stage')
        lst_prov = Bar(df, 'Provisions', 'Reporting_Year', colors='Stage')
        lst_lic = Bar(df, 'Lic', 'Reporting_Year', colors='Stage')
        coverage_ratio = LineDivision(df, 'Provisions', 'Ead_Airb', 'Reporting_Year', colors='Stage')
        lst_rwa = Bar(df, 'Rwa', 'Reporting_Year', colors='Stage')

        lst_ead.showlegend()

        obj.add_subplot(lst_ead, title='EAD EBA')
        obj.add_subplot(lst_ead_airb, title='EAD AIRB')
        obj.add_subplot(lst_rwa, title='RWA')
        obj.add_subplot(coverage_ratio, title='Coverage Ratio')
        obj.add_subplot(lst_prov, title='Provisions')
        obj.add_subplot(lst_lic, title='Loan Impairment Charges')

        obj.layout['barmode'] = 'relative'
        obj.layout['title'] = 'Results per stage'
        obj.stack()
        return obj

    @classmethod
    def from_csv(cls, path_to_csv):
        df = pd.read_csv(path_to_csv)
        return cls.from_df(df)


class RatingGradePane(Pane):
    def __init__(self, rating_grade_start_with):
        super().__init__(2, 3)
        self.sw = rating_grade_start_with

    @classmethod
    def from_df(cls, df, rating_grade_start_with):
        obj = RatingGradePane(rating_grade_start_with)

        df = df[df['Rating_Grade'].map(lambda x: x.startswith(obj.sw))].copy()

        lst_ead = Bar(df, 'Ead_Ifrs9', 'Reporting_Year', colors='Rating_Grade')
        lst_ead_airb = Bar(df, 'Ead_Airb', 'Reporting_Year', colors='Rating_Grade')
        lst_prov = Bar(df, 'Provisions', 'Reporting_Year', colors='Rating_Grade')
        lst_rwa_to_ead = LineDivision(df, 'Rwa', 'Ead_Airb', 'Reporting_Year', colors='Rating_Grade')
        coverage_ratio = LineDivision(df, 'Provisions', 'Ead_Airb', 'Reporting_Year', colors='Rating_Grade')
        lst_rwa = Bar(df, 'Rwa', 'Reporting_Year', colors='Rating_Grade')

        lst_ead.showlegend()

        obj.add_subplot(lst_ead, title='EAD IFRS9')
        obj.add_subplot(lst_ead_airb, title='EAD AIRB')
        obj.add_subplot(lst_rwa, title='RWA')
        obj.add_subplot(coverage_ratio, title='Coverage Ratio')
        obj.add_subplot(lst_prov, title='Provisions')
        obj.add_subplot(lst_rwa_to_ead, title='RWA To Ead AIRB')

        obj.layout['barmode'] = 'relative'
        obj.layout['title'] = 'Performing Rating Grade results'
        obj.stack()
        return obj

    @classmethod
    def from_csv(cls, path_to_csv, rating_grade_starts_with):
        df = pd.read_csv(path_to_csv)
        return cls.from_df(df, rating_grade_starts_with)


class CreditRiskComponentPane(Pane):
    """
    Very shortcut-y. Works for now
    """
    def __init__(self):
        super().__init__(1, 1)

    @classmethod
    def from_dataframe(cls, df):
        obj = CreditRiskComponentPane()
        obj.fig = make_component_plot(df)
        return obj

class ReconPane(Pane):

    def __init__(self):
        super().__init__(2, 2)

    def _define_figure(self):
        fig = tools.make_subplots(rows=self.n_rows, cols=self.n_cols,
                                  subplot_titles=self.titles, shared_yaxes=True)
        return fig

    @classmethod
    def from_dataframe(cls, df):
        obj = ReconPane()

        lst_prov = Bar(df, 'Provisions', 'Reporting_Year', colors='Stage')
        lst_prov_ifrs9 = Bar(df, 'Provision_Without_Tla', 'Reporting_Year', colors='Stage')
        lst_rwa = Bar(df, 'Rwa', 'Reporting_Year', colors='Stage')
        lst_rwa_ifrs9 = Bar(df, 'Ifrs9_Rwa', 'Reporting_Year', colors='Stage')

        lst_prov.showlegend()

        obj.add_subplot(lst_prov, title='Provisions Stress Test')
        obj.add_subplot(lst_prov_ifrs9, title='Provisions IFRS9')
        obj.add_subplot(lst_rwa, title='RWA Stress Test')
        obj.add_subplot(lst_rwa_ifrs9, title='RWA IFRS9')

        obj.layout['barmode'] = 'relative'
        obj.layout['title'] = 'Recon'
        obj.stack()
        return obj
class Page:
    def __init__(self, title, header):
        self.panes = list()
        self.title = title
        self.header = header

    def add_pane(self, pane):
        self.panes.append(pane)

    def full_header(self):
        return f"""<head><title>{self.title}</title></head>
                   <body><h1>{self.header}</h1></body>"""

    def to_string(self):
        output_string = ""
        for pane in self.panes:
            if not output_string:
                output_string += pane.full_html()
            else:
                output_string += pane.div_only()
        return self.full_header() + output_string

    def to_html(self, filename):
        output_string = self.to_string()
        with open(filename, 'w') as f:
            f.write(output_string)


class DartOutputPage(Page):
    def __init__(self, title, header):
        super().__init__(title, header)

    @classmethod
    def from_dfs(cls, df_agg, df_crps, title, header):
        page = DartOutputPage(title, header)

        stage_pane = StagePane.from_df(df_agg)
        rg_pane_perf = RatingGradePane.from_df(df_agg, rating_grade_start_with='R')
        rg_pane_non_perf = RatingGradePane.from_df(df_agg, rating_grade_start_with='D')
        recon_page = ReconPane.from_dataframe(df_agg)
        page.add_pane(stage_pane)
        page.add_pane(rg_pane_perf)
        page.add_pane(rg_pane_non_perf)
        page.add_pane(recon_page)

        try:
            component_pane = CreditRiskComponentPane.from_dataframe(df_crps)
            page.add_pane(component_pane)
        except Exception:
            print('no component plot today. Bad luck!')

        return page

    @classmethod
    def from_csvs(cls, path_to_agg, path_to_crps):
        df_agg = pd.read_csv(path_to_agg)
        df_crps = pd.read_csv(path_to_crps)
        return cls.from_dfs(df_agg, df_crps)

def run_id_to_titles(run_id):
    return f"{run_id.get('')}"


def main():
    scenario = 'EBA_2018_Baseline_2'
    run_type = 'EBA-PF-Cure-BL-fix'
    data_version = 'v23'
    run_date = '20180510'
    portfolio_run = 'RSME'

    parent_directory = r'T:\RSME\v23\output\RSME-EBA-PF-Cure-BL-fix-EBA_2018_Baseline_2_20180510-105539'
    dart_agg_output_name = 'Agg_output_normal_RSME_EBA_2018_Baseline_2_23_20180511031329.csv'
    dart_crps_output_name = 'Agg_crps_RSME_EBA_2018_Baseline_2_23_20180511031329.csv'
    outname = 'out_standalone.html'

    run_id = dict(
        scenario=scenario,
        run_type=run_type,
        data_version=data_version,
        run_date=run_date,
        portf_run=portfolio_run
    )

    title = '_'.join(run_id.values())
    header = '<br>'.join([f'{k}: {v}' for k, v in run_id.items()])

    df_normal = pd.read_csv(os.path.join(parent_directory, dart_agg_output_name))
    df_crps = pd.read_csv(os.path.join(parent_directory, dart_crps_output_name))

    outpage = DartOutputPage.from_dfs(df_normal, df_crps, title, header)
    outpage.to_html(os.path.join(parent_directory, outname))


if __name__ == '__main__':
    main()
