from wtforms import (
    DecimalField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, NumberRange, Optional

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.space_edit import SpaceEditForm
from observatory.models.mapper import EnumConvert, EnumHorizon
from observatory.models.sensor import Sensor

# pylint: disable=arguments-differ
# pylint: disable=no-member


class SpaceEditSensorsForm(SpaceEditForm):
    KEYS = {}
    SENSORS = []

    @staticmethod
    def sensor_fields(label):
        return (
            SelectField(
                label,
                coerce=int,
                validators=[DataRequired()],
                description='Select sensor',
            ),
            DecimalField(
                'Elevate',
                default=1.0,
                places=4,
                validators=[NumberRange(min=0.0)],
                description='Increase raw value with this factor',
            ),
            SelectField(
                'Convert',
                coerce=str,
                choices=[(en.name, en.name) for en in EnumConvert],
                validators=[DataRequired()],
                description='Select conversion',
            ),
            SelectField(
                'Horizon',
                coerce=str,
                choices=[(en.name, en.name) for en in EnumHorizon],
                validators=[DataRequired()],
                description='Select horizon',
            ),
        )

    @staticmethod
    def _sensor_choices():
        return [
            (sensor.prime, f'{sensor.slug} ({sensor.title})')
            for sensor in Sensor.query.order_by('slug').all()
        ]

    @staticmethod
    def _wind_speed_gust_unit_choices():
        return [(val, val) for val in ('m/s', 'km/h', 'kn')]

    def __init__(self, idx, *args, **kwargs):
        super().__init__(*args, idx=idx, **kwargs)

        for key in self.SENSORS:
            sensor_sel = getattr(self, key, None)
            if sensor_sel:
                sensor_sel.choices = self._sensor_choices()


class SpaceEditSensorsTemperatureForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.temperature.value',
        elevate='sensors.temperature.value.elevate',
        convert_sel='sensors.temperature.value.convert',
        horizon_sel='sensors.temperature.value.horizon',
        unit_sel='sensors.temperature.unit',
        location='sensors.temperature.location',
        name='sensors.temperature.name',
        description='sensors.temperature.description',
    )
    SENSORS = ['sensor_sel']

    (
        sensor_sel,
        elevate,
        convert_sel,
        horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Temperature sensor')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[
            (val, val)
            for val in ('°C', '°F', 'K', '°De', '°N', '°R', '°Ré', '°Rø')
        ],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsDoorLockedForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.door_locked.value',
        elevate='sensors.door_locked.value.elevate',
        convert_sel='sensors.door_locked.value.convert',
        horizon_sel='sensors.door_locked.value.horizon',
        location='sensors.door_locked.location',
        name='sensors.door_locked.name',
        description='sensors.door_locked.description',
    )
    SENSORS = ['sensor_sel']

    (
        sensor_sel,
        elevate,
        convert_sel,
        horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Door lock sensor')
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsBarometerForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.barometer.value',
        elevate='sensors.barometer.value.elevate',
        convert_sel='sensors.barometer.value.convert',
        horizon_sel='sensors.barometer.value.horizon',
        unit_sel='sensors.barometer.unit',
        location='sensors.barometer.location',
        name='sensors.barometer.name',
        description='sensors.barometer.description',
    )
    SENSORS = ['sensor_sel']

    (
        sensor_sel,
        elevate,
        convert_sel,
        horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Barometer')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[(val, val) for val in ('hPa', 'hPA')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsRadiationForm(SpaceEditSensorsForm):
    KEYS = []
    SENSORS = ['sensor_sel']

    @staticmethod
    def create(sub):
        return dict(
            sensor_sel=f'sensors.radiation.{sub}.value',
            elevate=f'sensors.radiation.{sub}.value.elevate',
            convert_sel=f'sensors.radiation.{sub}.value.convert',
            horizon_sel=f'sensors.radiation.{sub}.value.horizon',
            unit_sel=f'sensors.radiation.{sub}.unit',
            dead_time=f'sensors.radiation.{sub}.dead_time',
            conversion_factor=f'sensors.radiation.{sub}.conversion_factor',
            location=f'sensors.radiation.{sub}.location',
            name=f'sensors.radiation.{sub}.name',
            description=f'sensors.radiation.{sub}.description',
        )

    (
        sensor_sel,
        elevate,
        convert_sel,
        horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Radiation sensor')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[
            (val, val) for val in ('cpm', 'r/h', 'µSv/h', 'mSv/a', 'µSv/a')
        ],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    dead_time = DecimalField(
        'Dead time',
        default=1.0,
        places=6,
        validators=[NumberRange(min=0.0)],
        description='The dead time in µs',
    )
    conversion_factor = DecimalField(
        'Conversion factor',
        default=1.0,
        places=6,
        validators=[NumberRange(min=0.0)],
        description='Conversion from the cpm unit to another unit',
    )
    location = StringField(
        'Location',
        validators=[Optional()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsRadiationAlphaForm(SpaceEditSensorsRadiationForm):
    KEYS = SpaceEditSensorsRadiationForm.create('alpha')


class SpaceEditSensorsRadiationBetaForm(SpaceEditSensorsRadiationForm):
    KEYS = SpaceEditSensorsRadiationForm.create('beta')


class SpaceEditSensorsRadiationGammaForm(SpaceEditSensorsRadiationForm):
    KEYS = SpaceEditSensorsRadiationForm.create('gamma')


class SpaceEditSensorsRadiationBetaGammaForm(SpaceEditSensorsRadiationForm):
    KEYS = SpaceEditSensorsRadiationForm.create('beta_gamma')


class SpaceEditSensorsHumidityForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.humidity.value',
        elevate='sensors.humidity.value.elevate',
        convert_sel='sensors.humidity.value.convert',
        horizon_sel='sensors.humidity.value.horizon',
        unit_sel='sensors.humidity.unit',
        location='sensors.humidity.location',
        name='sensors.humidity.name',
        description='sensors.humidity.description',
    )
    SENSORS = ['sensor_sel']

    (
        sensor_sel,
        elevate,
        convert_sel,
        horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Humidity sensor')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[('%', '%')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsBeverageSupplyForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.beverage_supply.value',
        elevate='sensors.beverage_supply.value.elevate',
        convert_sel='sensors.beverage_supply.value.convert',
        horizon_sel='sensors.beverage_supply.value.horizon',
        unit_sel='sensors.beverage_supply.unit',
        location='sensors.beverage_supply.location',
        name='sensors.beverage_supply.name',
        description='sensors.beverage_supply.description',
    )
    SENSORS = ['sensor_sel']

    (
        sensor_sel,
        elevate,
        convert_sel,
        horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields(
        'How much Mate and beer is in your fridge?'
    )
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[('btl', 'Bottles'), ('crt', 'Crates')],
        validators=[DataRequired()],
        description='The unit (bottles or crates)',
    )
    location = StringField(
        'Location',
        validators=[Optional()],
        description='Where do you hide your gems',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='What is it',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsPowerConsumptionForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.power_consumption.value',
        elevate='sensors.power_consumption.value.elevate',
        convert_sel='sensors.power_consumption.value.convert',
        horizon_sel='sensors.power_consumption.value.horizon',
        unit_sel='sensors.power_consumption.unit',
        location='sensors.power_consumption.location',
        name='sensors.power_consumption.name',
        description='sensors.power_consumption.description',
    )
    SENSORS = ['sensor_sel']

    (
        sensor_sel,
        elevate,
        convert_sel,
        horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Power consumption')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[(val, val) for val in ('mW', 'W', 'VA')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsWindForm(SpaceEditSensorsForm):
    KEYS = dict(
        speed_sensor_sel='sensors.wind.properties.speed.value',
        speed_elevate='sensors.wind.properties.speed.value.elevate',
        speed_convert_sel='sensors.wind.properties.speed.value.convert',
        speed_horizon_sel='sensors.wind.properties.speed.value.horizon',
        speed_unit_sel='sensors.wind.properties.speed.unit',
        gust_sensor_sel='sensors.wind.properties.gust.value',
        gust_elevate='sensors.wind.properties.gust.value.elevate',
        gust_convert_sel='sensors.wind.properties.gust.value.convert',
        gust_horizon_sel='sensors.wind.properties.gust.value.horizon',
        gust_unit_sel='sensors.wind.properties.gust.unit',
        direction_sensor_sel='sensors.wind.properties.direction.value',
        direction_elevate='sensors.wind.properties.direction.value.elevate',
        direction_convert_sel=(
            'sensors.wind.properties.direction.value.convert'
        ),
        direction_horizon_sel=(
            'sensors.wind.properties.direction.value.horizon'
        ),
        direction_unit_sel='sensors.wind.properties.direction.unit',
        elevation_sensor_sel='sensors.wind.properties.elevation.value',
        elevation_elevate='sensors.wind.properties.elevation.value.elevate',
        elevation_convert_sel=(
            'sensors.wind.properties.elevation.value.convert'
        ),
        elevation_horizon_sel=(
            'sensors.wind.properties.elevation.value.horizon'
        ),
        elevation_unit_sel='sensors.wind.properties.elevation.unit',
        location='sensors.wind.location',
        name='sensors.wind.name',
        description='sensors.wind.description',
    )
    SENSORS = [
        'speed_sensor_sel',
        'gust_sensor_sel',
        'direction_sensor_sel',
        'elevation_sensor_sel',
    ]

    (
        speed_sensor_sel,
        speed_elevate,
        speed_convert_sel,
        speed_horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Wind speed sensor')
    speed_unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=SpaceEditSensorsForm._wind_speed_gust_unit_choices(),
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    (
        gust_sensor_sel,
        gust_elevate,
        gust_convert_sel,
        gust_horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Wind gust sensor')
    gust_unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=SpaceEditSensorsForm._wind_speed_gust_unit_choices(),
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    (
        direction_sensor_sel,
        direction_elevate,
        direction_convert_sel,
        direction_horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Wind direction sensor')
    direction_unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[('°', '°')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    (
        elevation_sensor_sel,
        elevation_elevate,
        elevation_convert_sel,
        elevation_horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Wind elevation sensor')
    elevation_unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[('m', 'm')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsAccountBalanceForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.account_balance.value',
        elevate='sensors.account_balance.value.elevate',
        convert_sel='sensors.account_balance.value.convert',
        horizon_sel='sensors.account_balance.value.horizon',
        unit_sel='sensors.account_balance.unit',
        location='sensors.account_balance.location',
        name='sensors.account_balance.name',
        description='sensors.account_balance.description',
    )
    SENSORS = ['sensor_sel']

    (
        sensor_sel,
        elevate,
        convert_sel,
        horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Account balance')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=SpaceEditSensorsForm._currency_choices(),
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[Optional()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsTotalMemberCountForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.total_member_count.value',
        elevate='sensors.total_member_count.value.elevate',
        convert_sel='sensors.total_member_count.value.convert',
        horizon_sel='sensors.total_member_count.value.horizon',
        location='sensors.total_member_count.location',
        name='sensors.total_member_count.name',
        description='sensors.total_member_count.description',
    )
    SENSORS = ['sensor_sel']

    (
        sensor_sel,
        elevate,
        convert_sel,
        horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Total member count')
    location = StringField(
        'Location',
        validators=[Optional()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsNetworkTrafficForm(SpaceEditSensorsForm):
    KEYS = dict(
        bps_sensor_sel=(
            'sensors.network_traffic.properties.bits_per_second.value'
        ),
        bps_elevate=(
            'sensors.network_traffic.properties.bits_per_second.value.elevate'
        ),
        bps_convert_sel=(
            'sensors.network_traffic.properties.bits_per_second.value.convert'
        ),
        bps_horizon_sel=(
            'sensors.network_traffic.properties.bits_per_second.value.horizon'
        ),
        bps_maximum=(
            'sensors.network_traffic.properties.bits_per_second.maximum'
        ),
        pps_sensor_sel=(
            'sensors.network_traffic.properties.packets_per_second.value'
        ),
        pps_elevate=(
            'sensors.network_traffic.properties.'
            'packets_per_second.value.elevate'
        ),
        pps_convert_sel=(
            'sensors.network_traffic.properties.'
            'packets_per_second.value.convert'
        ),
        pps_horizon_sel=(
            'sensors.network_traffic.properties.'
            'packets_per_second.value.horizon'
        ),
        location='sensors.network_traffic.location',
        name='sensors.network_traffic.name',
        description='sensors.network_traffic.description',
    )
    SENSORS = [
        'bps_sensor_sel',
        'pps_sensor_sel',
    ]

    (
        bps_sensor_sel,
        bps_elevate,
        bps_convert_sel,
        bps_horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Bits per second')
    bps_maximum = DecimalField(
        'Maximum bits per second',
        default=0.0,
        places=4,
        validators=[NumberRange(min=0.0)],
        description='E.g. as sold by your ISP',
    )
    (
        pps_sensor_sel,
        pps_elevate,
        pps_convert_sel,
        pps_horizon_sel,
    ) = SpaceEditSensorsForm.sensor_fields('Packages per second')
    location = StringField(
        'Location',
        validators=[Optional()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )
