import type {
	ILoginRequest,
	IRegistrationRequest,
	IAuthResponse,
	IUser,
	IMessageResponse,
} from './types';

import { createAction, createAsyncThunk } from '@reduxjs/toolkit';
import { login, registration, getUser } from '../../shared/api/user';

import { setIsAuthChecked } from './reducer';

export const loginUser = createAsyncThunk<IAuthResponse, ILoginRequest>(
	'user/login',
	login
);

export const registerUser = createAsyncThunk<
	IAuthResponse,
	IRegistrationRequest
>('user/registration', registration);

export const setUser = createAction<IUser | null>('auth/setUser');

export const checkUserAuth = createAsyncThunk(
	'user/checkUser',
	async (_, { dispatch }) => {
		if (localStorage.getItem('accessToken')) {
			try {
				const user = await getUser();
				dispatch(setUser(user || null));
			} catch (error) {
				dispatch(setUser(null));
			} finally {
				dispatch(setIsAuthChecked(true));
			}
		} else {
			dispatch(setIsAuthChecked(true));
		}
	}
);

export const logoutUser = createAsyncThunk<IMessageResponse>(
	'auth/logout',
	async () => {
		localStorage.removeItem('accessToken');
		return { message: 'Logged out' };
	}
);
