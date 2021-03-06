from flask import url_for
from pytest import mark

from observatory.models.mapper import Mapper

ENDPOINT = 'mgnt.drop_mapper'
VIEW_EP = 'mgnt.view_mapper'


@mark.usefixtures('session')
class TestMgntDropMapper:
    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert (
            url_for(
                ENDPOINT,
                prompt_slug='test',
                sensor_slug='demo',
            )
            == '/manage/mapper/drop/prompt/test/sensor/demo'
        )

    @staticmethod
    def test_no_user(visitor):
        visitor(
            ENDPOINT,
            method='post',
            params={
                'prompt_slug': 'prompt',
                'sensor_slug': 'sensor',
            },
            code=401,
        )

    @staticmethod
    def test_form_params(visitor, gen_user_loggedin, gen_prompt, gen_sensor):
        gen_user_loggedin()
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        url = url_for(
            ENDPOINT,
            prompt_slug=mapper.prompt.slug,
            sensor_slug=mapper.sensor.slug,
            _external=True,
        )
        res = visitor(VIEW_EP)
        form = res.soup.select(f'form[action="{url}"]')[-1]
        assert form['method'] == 'POST'

    @staticmethod
    def test_form_fields(visitor, gen_user_loggedin, gen_prompt, gen_sensor):
        gen_user_loggedin()
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        url = url_for(
            ENDPOINT,
            prompt_slug=mapper.prompt.slug,
            sensor_slug=mapper.sensor.slug,
            _external=True,
        )
        res = visitor(VIEW_EP)
        form = res.soup.select(f'form[action="{url}"]')[-1]
        button = form.select('button')[-1]
        assert button.attrs.get('name') == 'submit'
        assert button.attrs.get('type') == 'submit'

    @staticmethod
    def test_form_no_slug(visitor, gen_user_loggedin):
        gen_user_loggedin()
        slug = '🦔'

        res = visitor(
            ENDPOINT,
            method='post',
            params={
                'sensor_slug': slug,
                'prompt_slug': slug,
            },
            code=500,
        )

        assert 'no such mapper' in res.soup.text.lower()

    @staticmethod
    def test_form_deletes(visitor, gen_user_loggedin, gen_prompt, gen_sensor):
        gen_user_loggedin()
        prompt = gen_prompt()
        sensor = gen_sensor()
        mapper = Mapper.create(prompt=prompt, sensor=sensor)
        view_url = url_for(VIEW_EP, _external=True)

        assert Mapper.query.all() == [mapper]
        res = visitor(
            ENDPOINT,
            method='post',
            params={
                'sensor_slug': prompt.slug,
                'prompt_slug': sensor.slug,
            },
            code=302,
        )

        assert res.request.headers['LOCATION'] == view_url
        assert Mapper.query.all() == []
