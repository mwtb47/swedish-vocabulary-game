"""Script to create dashboard."""

from dash import Dash
import dash_bootstrap_components as dbc

from dashboard.components.layout import create_layout
from dashboard.data import Data


db_data = Data()


def main() -> None:

    app = Dash(
        __name__,
        use_pages=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
    )
    app.layout = create_layout()
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
