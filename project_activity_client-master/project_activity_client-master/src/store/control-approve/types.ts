import type { IRole, IDepartment } from '../catalog/types';

export interface IControlApproveStore {
	approveUsers: IApproveUser[];
	currentApproveUser: IApproveUser | null;
	isOpenApproveModal: boolean;
	isOpenRejectModal: boolean;
	isOpenDetailModal: boolean;
	isLoadingApprove: boolean;
	isLoadingRequest: boolean;
	error: string | null;
}

export interface IApproveUser {
	id: number;
	first_name: string;
	last_name: string;
	middle_name: string;
	email: string;
	phone: string;
	comment: string;
	created_at: string;
	status: 'submitted' | 'approved' | 'rejected';
	role?: IRole;
	department?: IDepartment;
	actor?: { id: number; full_name: string; email: string };
	reason?: string;
}

export interface IApproveUserRequest {
	userId: number;
	role_id: string;
	department_id: number;
}

export interface IRejectUserRequest {
	userId: number;
	reason: string;
}
