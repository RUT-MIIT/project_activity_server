import { API_URL } from '../config';

const checkResponse = (res: Response) => {
	return res.ok ? res.json() : res.json().then((err) => Promise.reject(err));
};

export const request = (endpoint: string, options: RequestInit) => {
	return fetch(`${API_URL}${endpoint}`, options).then(checkResponse);
};
