import type {
	IApproveUserRequest,
	IRejectUserRequest,
} from '../../store/control-approve/types';

import { request } from './utils';

export const getApproveUsers = () => {
	return request('/accounts/registration-requests/', {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
		},
	});
};

export const approveUser = (data: IApproveUserRequest) => {
	return request(`/accounts/registration-requests/${data.userId}/approve/`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
		},
		body: JSON.stringify({
			role_id: data.role_id,
			department_id: data.department_id,
		}),
	});
};

export const rejectUser = (data: IRejectUserRequest) => {
	console.log(data);
	return request(`/accounts/registration-requests/${data.userId}/reject/`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
		},
		body: JSON.stringify({ reason: data.reason }),
	});
};
