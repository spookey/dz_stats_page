from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.generic import GenericDropForm, GenericSortForm
from observatory.models.mapper import (
    EnumColor,
    EnumConvert,
    EnumHorizon,
    Mapper,
)
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor

# pylint: disable=arguments-differ
# pylint: disable=no-member


class MapperEditForm(FlaskForm):
    prompt_sel = SelectField(
        'Prompt',
        coerce=int,
        validators=[DataRequired()],
        description='Select prompt',
    )
    sensor_sel = SelectField(
        'Sensor',
        coerce=int,
        validators=[DataRequired()],
        description='Select sensor',
    )
    active = BooleanField(
        'Active',
        default=True,
        description='Set active',
    )
    elevate = DecimalField(
        'Elevate',
        default=1.0,
        places=4,
        validators=[NumberRange(min=0.0)],
        description='Increase raw value with this factor',
    )
    color_sel = SelectField(
        'Color',
        coerce=str,
        validators=[DataRequired()],
        description='Select color',
        render_kw={'data_colorize': 'option'},
    )
    convert_sel = SelectField(
        'Convert',
        coerce=int,
        validators=[DataRequired()],
        description='Select conversion',
    )
    horizon_sel = SelectField(
        'Horizon',
        coerce=int,
        validators=[DataRequired()],
        description='Select horizon',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )

    @staticmethod
    def _comm_choices(model):
        return [
            (cm.prime, f'{cm.slug} ({cm.title})')
            for cm in model.query.order_by('slug').all()
        ]

    @staticmethod
    def _color_choices():
        return [(en.color, en.name) for en in EnumColor]

    @staticmethod
    def _translate_choices(enum):
        return [(en.value, en.name) for en in enum]

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.mapper = obj

        self.prompt_sel.choices = self._comm_choices(Prompt)
        self.sensor_sel.choices = self._comm_choices(Sensor)

        self.color_sel.choices = self._color_choices()
        self.convert_sel.choices = self._translate_choices(EnumConvert)
        self.horizon_sel.choices = self._translate_choices(EnumHorizon)

    def set_selections(self):
        if not self.mapper:
            return
        self.prompt_sel.data = self.mapper.prompt_prime
        self.sensor_sel.data = self.mapper.sensor_prime

        self.color_sel.data = self.mapper.color.color
        self.convert_sel.data = self.mapper.convert.value
        self.horizon_sel.data = self.mapper.horizon.value

    def validate(self):
        if not super().validate():
            return False

        def comm_err(msg):
            self.prompt_sel.errors.append(msg)
            self.sensor_sel.errors.append(msg)

        mapper = Mapper.by_commons(
            prompt=Prompt.by_prime(self.prompt_sel.data),
            sensor=Sensor.by_prime(self.sensor_sel.data),
        )
        if mapper is not None:
            if self.mapper is None:
                comm_err('Combination already present!')
                return False

            if (
                self.mapper.prompt.prime != mapper.prompt.prime
                and self.mapper.sensor.prime != mapper.sensor.prime
            ):
                comm_err('Combination conflict!')
                return False

        return True

    def action(self):
        if not self.validate():
            return None

        if not self.mapper:
            self.mapper = Mapper.create(
                prompt=Prompt.by_prime(self.prompt_sel.data),
                sensor=Sensor.by_prime(self.sensor_sel.data),
                _commit=False,
            )

        self.populate_obj(self.mapper)
        self.mapper.color = EnumColor.from_color(self.color_sel.data)
        self.mapper.convert = EnumConvert(self.convert_sel.data)
        self.mapper.horizon = EnumHorizon(self.horizon_sel.data)
        return self.mapper.save()


class MapperDropForm(GenericDropForm):
    Model = Mapper


class MapperSortForm(GenericSortForm):
    Model = Mapper
