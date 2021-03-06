from logging import getLogger

from flask import current_app, render_template, request, url_for
from jinja2 import Markup

from observatory.forms.common import (
    PromptDropForm,
    PromptSortForm,
    SensorDropForm,
    SensorSortForm,
)
from observatory.forms.mapper import MapperDropForm, MapperSortForm
from observatory.forms.space_drop import (
    SpaceDropCamForm,
    SpaceDropContactKeymastersForm,
    SpaceDropLinksForm,
    SpaceDropMembershipPlansForm,
    SpaceDropProjectsForm,
    SpaceDropSensorsAccountBalanceForm,
    SpaceDropSensorsBarometerForm,
    SpaceDropSensorsBeverageSupplyForm,
    SpaceDropSensorsDoorLockedForm,
    SpaceDropSensorsHumidityForm,
    SpaceDropSensorsNetworkTrafficForm,
    SpaceDropSensorsPowerConsumptionForm,
    SpaceDropSensorsRadiationAlphaForm,
    SpaceDropSensorsRadiationBetaForm,
    SpaceDropSensorsRadiationBetaGammaForm,
    SpaceDropSensorsRadiationGammaForm,
    SpaceDropSensorsTemperatureForm,
    SpaceDropSensorsTotalMemberCountForm,
    SpaceDropSensorsWindForm,
)
from observatory.lib.text import random_line
from observatory.start.environment import (
    API_PLOT_REFRESH_MS,
    FMT_MOMENT_DAY,
    FMT_MOMENT_DEFAULT,
    FMT_MOMENT_HOUR,
    FMT_MOMENT_MINUTE,
    FMT_MOMENT_MONTH,
    FMT_MOMENT_MSECOND,
    FMT_MOMENT_QUARTER,
    FMT_MOMENT_SECOND,
    FMT_MOMENT_WEEK,
    FMT_MOMENT_YEAR,
    TAGLINES,
)

LOG = getLogger(__name__)


def errorhandler(error):
    LOG.error(
        'handling error "%s" - "%s" for "%s %s"',
        error.code,
        error.description,
        request.method,
        request.url,
    )

    return (
        render_template(
            'error.html',
            error=error,
            title=error.code,
        ),
        error.code,
    )


def tagline():
    return Markup(random_line(TAGLINES))


def script_config_data():
    api_plot_base_url = url_for('api.charts.plot', slug='', _external=True)
    api_space_api_url = (
        url_for('api.sp_api.json', _external=True)
        if current_app.config.get('SP_API_ENABLE', False)
        else ''
    )

    return Markup(
        ' '.join(
            line.strip()
            for line in f'''
data-api-plot-base-url="{api_plot_base_url}"
data-api-plot-refresh-ms="{API_PLOT_REFRESH_MS}"
data-api-space-api-url="{api_space_api_url}"
data-moment-default-format="{FMT_MOMENT_DEFAULT}"
data-moment-msecond-format="{FMT_MOMENT_MSECOND}"
data-moment-second-format="{FMT_MOMENT_SECOND}"
data-moment-minute-format="{FMT_MOMENT_MINUTE}"
data-moment-hour-format="{FMT_MOMENT_HOUR}"
data-moment-day-format="{FMT_MOMENT_DAY}"
data-moment-week-format="{FMT_MOMENT_WEEK}"
data-moment-month-format="{FMT_MOMENT_MONTH}"
data-moment-quarter-format="{FMT_MOMENT_QUARTER}"
data-moment-year-format="{FMT_MOMENT_YEAR}"
    '''.splitlines()
        ).strip()
    )


def form_drop_mapper(mapper):
    return MapperDropForm(obj=mapper)


def form_drop_prompt(prompt):
    return PromptDropForm(obj=prompt)


def form_drop_sensor(sensor):
    return SensorDropForm(obj=sensor)


def form_sort_mapper(mapper, lift):
    return MapperSortForm(obj=mapper, lift=lift)


def form_sort_prompt(prompt, lift):
    return PromptSortForm(obj=prompt, lift=lift)


def form_sort_sensor(sensor, lift):
    return SensorSortForm(obj=sensor, lift=lift)


def form_drop_space_cam(idx):
    return SpaceDropCamForm(idx=idx)


def form_drop_space_contact_keymasters(idx):
    return SpaceDropContactKeymastersForm(idx=idx)


def form_drop_space_sensors_temperature(idx):
    return SpaceDropSensorsTemperatureForm(idx=idx)


def form_drop_space_sensors_door_locked(idx):
    return SpaceDropSensorsDoorLockedForm(idx=idx)


def form_drop_space_sensors_barometer(idx):
    return SpaceDropSensorsBarometerForm(idx=idx)


def form_drop_space_sensors_radiation_alpha(idx):
    return SpaceDropSensorsRadiationAlphaForm(idx=idx)


def form_drop_space_sensors_radiation_beta(idx):
    return SpaceDropSensorsRadiationBetaForm(idx=idx)


def form_drop_space_sensors_radiation_gamma(idx):
    return SpaceDropSensorsRadiationGammaForm(idx=idx)


def form_drop_space_sensors_radiation_beta_gamma(idx):
    return SpaceDropSensorsRadiationBetaGammaForm(idx=idx)


def form_drop_space_sensors_humidity(idx):
    return SpaceDropSensorsHumidityForm(idx=idx)


def form_drop_space_sensors_beverage_supply(idx):
    return SpaceDropSensorsBeverageSupplyForm(idx=idx)


def form_drop_space_sensors_power_consumption(idx):
    return SpaceDropSensorsPowerConsumptionForm(idx=idx)


def form_drop_space_sensors_wind(idx):
    return SpaceDropSensorsWindForm(idx=idx)


def form_drop_space_sensors_account_balance(idx):
    return SpaceDropSensorsAccountBalanceForm(idx=idx)


def form_drop_space_sensors_total_member_count(idx):
    return SpaceDropSensorsTotalMemberCountForm(idx=idx)


def form_drop_space_sensors_network_traffic(idx):
    return SpaceDropSensorsNetworkTrafficForm(idx=idx)


def form_drop_space_links(idx):
    return SpaceDropLinksForm(idx=idx)


def form_drop_space_membership_plans(idx):
    return SpaceDropMembershipPlansForm(idx=idx)


def form_drop_space_projects(idx):
    return SpaceDropProjectsForm(idx=idx)
