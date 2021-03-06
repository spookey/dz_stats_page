from observatory.forms.base import BaseForm
from observatory.instance import SPACE_API
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX

# pylint: disable=arguments-differ
# pylint: disable=no-member


class SpaceDropForm(BaseForm):
    KEYS = []

    submit = BaseForm.gen_submit_button(
        'Delete',
        icon='ops_delete',
        classreplace_kw={'is-dark': 'is-danger is-small'},
    )

    def __init__(self, *args, idx, **kwargs):
        super().__init__(*args, **kwargs)
        self.idx = idx

    def validate(self):
        return super().validate() and self.idx is not None

    def action(self):
        if not self.validate():
            return None

        results = [
            elem.delete()
            for elem in [
                Value.by_key_idx(key=f'{SP_API_PREFIX}.{key}', idx=self.idx)
                for key in self.KEYS
            ]
            if elem is not None
        ]

        if not any(results):
            return None

        return SPACE_API.reset()


class SpaceDropCamForm(SpaceDropForm):
    KEYS = ['cam']


class SpaceDropContactKeymastersForm(SpaceDropForm):
    KEYS = [
        'contact.keymasters.name',
        'contact.keymasters.irc_nick',
        'contact.keymasters.phone',
        'contact.keymasters.email',
        'contact.keymasters.twitter',
        'contact.keymasters.xmpp',
        'contact.keymasters.mastodon',
        'contact.keymasters.matrix',
    ]


class SpaceDropSensorsTemperatureForm(SpaceDropForm):
    KEYS = [
        'sensors.temperature.value',
        'sensors.temperature.unit',
        'sensors.temperature.location',
        'sensors.temperature.name',
        'sensors.temperature.description',
    ]


class SpaceDropSensorsDoorLockedForm(SpaceDropForm):
    KEYS = [
        'sensors.door_locked.value',
        'sensors.door_locked.location',
        'sensors.door_locked.name',
        'sensors.door_locked.description',
    ]


class SpaceDropSensorsBarometerForm(SpaceDropForm):
    KEYS = [
        'sensors.barometer.value',
        'sensors.barometer.unit',
        'sensors.barometer.location',
        'sensors.barometer.name',
        'sensors.barometer.description',
    ]


class SpaceDropSensorsRadiationForm(SpaceDropForm):
    KEYS = []

    @staticmethod
    def create(sub):
        return [
            f'sensors.radiation.{sub}.value',
            f'sensors.radiation.{sub}.unit',
            f'sensors.radiation.{sub}.dead_time',
            f'sensors.radiation.{sub}.conversion_factor',
            f'sensors.radiation.{sub}.location',
            f'sensors.radiation.{sub}.name',
            f'sensors.radiation.{sub}.description',
        ]


class SpaceDropSensorsRadiationAlphaForm(SpaceDropSensorsRadiationForm):
    KEYS = SpaceDropSensorsRadiationForm.create('alpha')


class SpaceDropSensorsRadiationBetaForm(SpaceDropSensorsRadiationForm):
    KEYS = SpaceDropSensorsRadiationForm.create('beta')


class SpaceDropSensorsRadiationGammaForm(SpaceDropSensorsRadiationForm):
    KEYS = SpaceDropSensorsRadiationForm.create('gamma')


class SpaceDropSensorsRadiationBetaGammaForm(SpaceDropSensorsRadiationForm):
    KEYS = SpaceDropSensorsRadiationForm.create('beta_gamma')


class SpaceDropSensorsHumidityForm(SpaceDropForm):
    KEYS = [
        'sensors.humidity.value',
        'sensors.humidity.unit',
        'sensors.humidity.location',
        'sensors.humidity.name',
        'sensors.humidity.description',
    ]


class SpaceDropSensorsBeverageSupplyForm(SpaceDropForm):
    KEYS = [
        'sensors.beverage_supply.value',
        'sensors.beverage_supply.unit',
        'sensors.beverage_supply.location',
        'sensors.beverage_supply.name',
        'sensors.beverage_supply.description',
    ]


class SpaceDropSensorsPowerConsumptionForm(SpaceDropForm):
    KEYS = [
        'sensors.power_consumption.value',
        'sensors.power_consumption.unit',
        'sensors.power_consumption.location',
        'sensors.power_consumption.name',
        'sensors.power_consumption.description',
    ]


class SpaceDropSensorsWindForm(SpaceDropForm):
    KEYS = [
        'sensors.wind.properties.speed.value',
        'sensors.wind.properties.speed.unit',
        'sensors.wind.properties.gust.value',
        'sensors.wind.properties.gust.unit',
        'sensors.wind.properties.direction.value',
        'sensors.wind.properties.direction.unit',
        'sensors.wind.properties.elevation.value',
        'sensors.wind.properties.elevation.unit',
        'sensors.wind.location',
        'sensors.wind.name',
        'sensors.wind.description',
    ]


class SpaceDropSensorsAccountBalanceForm(SpaceDropForm):
    KEYS = [
        'sensors.account_balance.value',
        'sensors.account_balance.unit',
        'sensors.account_balance.location',
        'sensors.account_balance.name',
        'sensors.account_balance.description',
    ]


class SpaceDropSensorsTotalMemberCountForm(SpaceDropForm):
    KEYS = [
        'sensors.total_member_count.value',
        'sensors.total_member_count.location',
        'sensors.total_member_count.name',
        'sensors.total_member_count.description',
    ]


class SpaceDropSensorsNetworkTrafficForm(SpaceDropForm):
    KEYS = [
        'sensors.network_traffic.properties.bits_per_second.value',
        'sensors.network_traffic.properties.bits_per_second.maximum',
        'sensors.network_traffic.properties.packets_per_second.value',
        'sensors.network_traffic.location',
        'sensors.network_traffic.name',
        'sensors.network_traffic.description',
    ]


class SpaceDropProjectsForm(SpaceDropForm):
    KEYS = ['projects']


class SpaceDropLinksForm(SpaceDropForm):
    KEYS = [
        'links.name',
        'links.description',
        'links.url',
    ]


class SpaceDropMembershipPlansForm(SpaceDropForm):
    KEYS = [
        'membership_plans.name',
        'membership_plans.value',
        'membership_plans.currency',
        'membership_plans.billing_interval',
        'membership_plans.description',
    ]
