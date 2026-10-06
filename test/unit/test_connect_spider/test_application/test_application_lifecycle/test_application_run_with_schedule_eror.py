from unittest.mock import Mock,patch
from src.application.application import Application

def test_application_run_with_schedule_error():
    target = 'src.application.application.logger'
    with patch(f'{target}.exception') as mock_exception:
        order = []
        orchestrator = Mock()
        reactor = Mock()
        pool = Mock()
        orchestrator.schedule.side_effect = Exception("Test exception")
        reactor.run.side_effect = lambda: order.append("reactor")
        application = Application(orchestrator, reactor,pool)
        application.run()
        mock_exception.assert_called_once_with("Error scheduling orchestrator: Test exception")
        reactor.run.assert_called_once()
        assert order == ["reactor"]
        
