#!/usr/bin/env python3
import flask_monitoringdashboard as dashboard
from app import create_app


if __name__ == "__main__":
    app = create_app()
    dashboard.bind(app)
    app.run(debug=True)

