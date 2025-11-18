export const getApiUrl = (): string => {
	const { hostname } = window.location;

	if (hostname === 'localhost') {
		return 'http://10.242.221.0:8000/api';
	} else if (hostname === 'cvo-test.emiit.ru') {
		return 'https://cvo-test-api.emiit.ru/api/v1';
	} else if (hostname === 'cvo.emiit.ru') {
		return 'https://cvo-api.emiit.ru/api/v1';
	}

	return 'http://10.242.224.105:8000/api/v1';
};

export const API_URL = getApiUrl();
