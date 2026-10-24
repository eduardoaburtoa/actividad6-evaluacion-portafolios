"""Prueba real de navegación e interacciones de Streamlit."""
from pathlib import Path
from streamlit.testing.v1 import AppTest
R=Path(__file__).resolve().parents[1]
def test_inicio_y_controles():
    app=AppTest.from_file(str(R/'app.py'),default_timeout=60).run()
    assert not app.exception
    assert len(app.tabs)==5
    assert len(app.metric)==4
    app.slider[0].set_value(.5).run()
    assert not app.exception
    app.number_input[0].set_value(5_000_000.0).run()
    app.slider[1].set_value(24).run()
    assert not app.exception
    assert any('200,000' in element.value for element in app.markdown)
