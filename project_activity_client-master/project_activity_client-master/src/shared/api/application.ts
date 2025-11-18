import type {
	ICreateAppMain,
	ICreateAppPublic,
} from '../../store/application/types';

import { request } from './utils';

export const getApplications = () => {
	return request('/showcase/project-applications/my_applications', {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
		},
	});
};

export const createMainApplication = (data: ICreateAppMain) => {
	return request('/showcase/project-applications/', {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
		},
		body: JSON.stringify(data),
	});
};

export const createPublicApplication = (data: ICreateAppPublic) => {
	return request('/showcase/project-applications/simple/', {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(data),
	});
};
