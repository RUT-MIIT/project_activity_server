export interface ILoginRequest {
	email: string;
	password: string;
}

export interface IRegistrationRequest {
	first_name: string;
	last_name: string;
	middle_name: string;
	email: string;
	phone: string;
	comment: string;
}

export interface IAuthResponse {
	access: string;
	refresh: string;
	user: IUser;
}

export interface IUser {
	id: number;
	email: string;
	first_name: string;
	last_name: string;
	middle_name: string;
	role: string;
	phone: string;
	department: {
		id: number;
		name: string;
		short_name: string;
	};
}

export interface IUserStore {
	user: IUser | null;
	isAuthChecked: boolean;
	isLoading: boolean;
	error: string | null;
}

export interface ITokenRequest {
	token: string;
}

export interface IMessageResponse {
	id?: number;
	message: string;
}
