import type { IEditApp } from '../../store/application/types';
import type { ICreateCommentAction } from '../../store/coordination/types';

import { request } from './utils';

export const getCoordinationApps = () => {
	return request('/showcase/project-applications/my_in_work/', {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
		},
	});
};

export const getCoordinationDetail = (id: string) => {
	return request(`/showcase/project-applications/${id}/`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
		},
	});
};

export const editApp = (id: number, data: IEditApp) => {
	return request(`/showcase/project-applications/${id}/`, {
		method: 'PATCH',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
		},
		body: JSON.stringify(data),
	});
};

export const createCommentToField = (data: ICreateCommentAction) => {
	return request(
		`/showcase/project-applications/${data.applicationId}/add_comment/`,
		{
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
			},
			body: JSON.stringify({ field: data.field, text: data.text }),
		}
	);
};

export const approveApp = (applicationId: number) => {
	return request(`/showcase/project-applications/${applicationId}/approve/`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
		},
	});
};

export const reworkApp = (applicationId: number) => {
	return request(
		`/showcase/project-applications/${applicationId}/request_changes/`,
		{
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
			},
		}
	);
};

export const rejectApp = (applicationId: number, reason: string) => {
	return request(`/showcase/project-applications/${applicationId}/reject/`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
		},
		body: JSON.stringify({ reason: reason }),
	});
};
