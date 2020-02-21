from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired

from stats.models.mapper import EnumAxis, EnumCast, EnumHorizon, Mapper
from stats.models.prompt import Prompt
from stats.models.sensor import Sensor


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
    axis_sel = SelectField(
        'Axis',
        coerce=int,
        validators=[DataRequired()],
        description='Select axis',
    )
    cast_sel = SelectField(
        'Cast',
        coerce=int,
        validators=[DataRequired()],
        description='Select cast',
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
    )

    @staticmethod
    def _comm_choices(model):
        return [
            (cm.prime, f'{cm.slug} ({cm.title})')
            for cm in model.query.order_by('slug').all()
        ]

    @staticmethod
    def _enum_choices(enum):
        return [
            (en.value, en.name)
            for en in enum
        ]

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.mapper = obj

        self.prompt_sel.choices = self._comm_choices(Prompt)
        self.sensor_sel.choices = self._comm_choices(Sensor)

        self.axis_sel.choices = self._enum_choices(EnumAxis)
        self.cast_sel.choices = self._enum_choices(EnumCast)
        self.horizon_sel.choices = self._enum_choices(EnumHorizon)

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
                    and
                    self.mapper.sensor.prime != mapper.sensor.prime
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
        self.mapper.axis = EnumAxis(self.axis_sel.data)
        self.mapper.cast = EnumCast(self.cast_sel.data)
        self.mapper.horizon = EnumHorizon(self.horizon_sel.data)
        return self.mapper.save()