from mock import Mock
from datetime import datetime

def create_datetime_mock(name, return_value = None):
	mocked_datetime = Mock()
	
	if return_value is not None:
		setattr(mocked_datetime, name, Mock(return_value = return_value))
	else:
		setattr(mocked_datetime, name, mocked_datetime)
	
	return mocked_datetime