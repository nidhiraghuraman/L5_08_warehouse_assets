
"""Warehouse asset maintenance registry.

Registers equipment, records service dates, identifies overdue inspections,
and exports maintenance reports.
"""

import json
import tempfile
from datetime import datetime, timedelta

assets = {}
SERVICE_INTERVAL_DAYS = 90
DATE_FORMAT = "%Y-%m-%d"


def register_asset(asset_id, machine_type, logs=None):
    """Register an asset without overwriting an existing asset."""
    if not asset_id or not asset_id.strip():
        print("Error: asset ID cannot be empty.")
        return

    if asset_id in assets:
        print(f"Error: asset {asset_id} is already registered.")
        return

    if logs is None:
        logs = []

    assets[asset_id] = {
        "type": machine_type,
        "last_service": datetime.now().strftime(DATE_FORMAT),
    }
    logs.append(asset_id)
    print(
        f"Registered {asset_id} - "
        f"total registrations this run: {len(logs)}"
    )


def update_service_date(asset_id, service_date):
    """Update an asset's service date after validating the input."""
    if asset_id not in assets:
        print(f"Error: asset {asset_id} is not registered.")
        return

    try:
        parsed_date = datetime.strptime(service_date, DATE_FORMAT)
    except ValueError:
        print(
            f"Error: invalid date '{service_date}'. "
            "Use YYYY-MM-DD."
        )
        return

    assets[asset_id]["last_service"] = parsed_date.strftime(DATE_FORMAT)
    print(f"Updated service date for {asset_id}.")


def due_for_inspection():
    """Return asset IDs whose last service was over the allowed interval ago."""
    due = []
    today = datetime.now()

    for asset_id, asset in assets.items():
        last_service = datetime.strptime(
            asset["last_service"], DATE_FORMAT
        )
        if today - last_service > timedelta(days=SERVICE_INTERVAL_DAYS):
            due.append(asset_id)

    return due


def change_interval(days):
    """Change the inspection interval to a positive whole number of days."""
    global SERVICE_INTERVAL_DAYS

    if isinstance(days, bool) or not isinstance(days, int) or days <= 0:
        raise ValueError("Inspection interval must be a positive integer.")

    SERVICE_INTERVAL_DAYS = days


def export_service_report(file="maintenance.json"):
    """Export the asset registry as formatted JSON."""
    with open(file, "w", encoding="utf-8") as report_file:
        json.dump(assets, report_file, indent=2)

    print(f"Report written to {file}")


def write_scratch_copy():
    """Write the registry to a securely created temporary JSON file."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        prefix="maintenance_",
        encoding="utf-8",
        delete=False,
    ) as scratch_file:
        json.dump(assets, scratch_file, indent=2)
        path = scratch_file.name

    print(f"Scratch copy at {path}")


def print_alerts():
    """Print alerts for assets with overdue inspections."""
    for asset_id in due_for_inspection():
        print(
            f"ALERT: inspection overdue for {asset_id} "
            f"({assets[asset_id]['type']})"
        )


def main():
    """Run the warehouse maintenance registry demonstration."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("PJ-03", "Pallet Jack")
    register_asset("FL-01", "Crane")

    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")

    try:
        change_interval(-30)
    except ValueError as error:
        print(f"Error: {error}. Using the default interval.")

    service_date = input(
        "Last service date for CV-07 (YYYY-MM-DD, Enter to skip): "
    ).strip()

    if service_date:
        update_service_date("CV-07", service_date)

    if not assets:
        print("No assets are registered.")
        return

    print_alerts()
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
